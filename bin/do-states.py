#!/usr/bin/env python3
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import os
import sys
import argparse
import uuid
import zmq
sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.debug
import lib.constants
import lib.config
import lib.transport
import lib.template
import lib.master_utils
import lib.db_sqlite3
import lib.hostname_ip
import simplejson
import re
import lib.slave_utils
import requests

parser = argparse.ArgumentParser(description="Command should be run on master")
parser.add_argument("-l","--list",dest="list",action="store_true",help="list all the states that are available")
parser.add_argument("-n","--hosts",dest="hosts",help="destination hosts to run the states on")
parser.add_argument("-s","--state",dest="state",help="state to run on the hosts")
parser.add_argument("-t","--test",dest="test",help="state to test")
args = parser.parse_args()


if(args.list):
  states = lib.template.states().list.keys()
  states.sort()
  for x in states:
    print(x)

else:
  if(args.state):
    lib.debug.debug("running state : "+ args.state)
    uid = str(uuid.uuid4())
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    socket.connect("ipc:///tmp/publisher.zmq.sock")
    socket.setsockopt(zmq.SNDTIMEO, 1000 * 2)
    # socket.send_multipart([uid,args.hosts,args.state])
    socket.send_multipart([uid.encode('utf-8'), args.hosts.encode('utf-8'), args.state.encode('utf-8')])
    validhosts = socket.recv_pyobj()
    socket.close()
    totalhosts = len(validhosts)
    if(validhosts):
      for x in validhosts:
        print (x +" : "+ simplejson.dumps(validhosts[x],indent=4))
    else:
      print("No valid hosts")
    if not re.match(r'^ping\.', args.state):

      hosts_file = os.path.join(lib.constants.m_result_logs_dir,lib.constants.m_result_logs_prefix_hosts + lib.constants.m_result_logs_delimiter + uid)
      hosts_file_fd = open(hosts_file,"w")
      hosts_file_fd.write(simplejson.dumps(validhosts))
      hosts_file_fd.flush()
      hosts_file_fd.close()


      lib.db_sqlite3.execute("insert into log "
                             "(request_id,state_name,topic) values "
                             "(\"{0}\",\"{1}\",\"{2}\")".format(uid,args.state,args.hosts),
                             db_file=lib.constants.m_dostates_sqlite3_file)
      print("request id : "+ str(uid))

    print("TOTAL : "+ str(totalhosts))

  elif(args.test):
    state_name = args.test
    lib.debug.debug("testing state : " + args.test)
    slaveconst = lib.slave_utils.slaveconst().slaveconst()
    requestStr = ""
    if (state_name != "high"):
      requestStr = "http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.slave_conf['master_rest_port']) + "/states/" + lib.hostname_ip.hostname + "/" + state_name + "/0"
      # r = requests.post("http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.slave_conf['master_rest_port']) + "/states/" + lib.hostname_ip.hostname + "/" + state_name + "/0", data=simplejson.dumps(slaveconst))
    else:
      requestStr = "http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.slave_conf['master_rest_port']) + "/high/" + lib.hostname_ip.hostname
      # r = requests.post("http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.slave_conf['master_rest_port']) + "/high/" + lib.hostname_ip.hostname, data=simplejson.dumps(slaveconst))
    lib.debug.info(requestStr)
    r = requests.post(requestStr, data=simplejson.dumps(slaveconst))
    try:
      rendered_state = simplejson.loads(r.content)
      print (simplejson.dumps(rendered_state, indent=4))
    except:
      print (r.content)


