#!/usr/bin/env python3
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.constants
import lib.db_sqlite3
import argparse
import glob
import simplejson
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-l","--list",dest="list",action="store_true",help="list all the logs")
parser.add_argument("-c","--clean",dest="clean",action="store_true",help="clean all the logs")
parser.add_argument("-k","--keep",dest="keep",help="keep only the last <n> number of logs. delete the rest")
parser.add_argument("-s","--show",dest="id",help="show the logs for id ...")
parser.add_argument("-t","--tail",dest="tail",action="store_true",help="tail the logs")
# parser.add_argument("-j","--jobs",dest="jobs")
args = parser.parse_args()


# ulogs = {}
# for x in logs:
#   ulogs[x.split(lib.constants.m_result_logs_delimiter)[-2]] = x
if(args.list):
  id_details = lib.db_sqlite3.execute("select * from log order by submit_time asc",
                                      db_file=lib.constants.m_dostates_sqlite3_file,
                                      dictionary=True)

  for x in id_details:
    print("\n")
    print(simplejson.dumps(x,indent=4))
else:
  if(args.id):
    id_details = lib.db_sqlite3.execute("select * from log where request_id=\"" + args.id +"\"",
                                        db_file=lib.constants.m_dostates_sqlite3_file,
                                        dictionary=True)

    host_detail = simplejson.loads(open(os.path.join(lib.constants.m_result_logs_dir, lib.constants.m_result_logs_prefix_hosts + lib.constants.m_result_logs_delimiter + args.id), "r").read())

    print(simplejson.dumps(id_details[0],indent=4))
    print(simplejson.dumps(host_detail, indent=4))
    files_to_open = glob.glob(os.path.join(lib.constants.m_result_logs_dir,lib.constants.m_result_logs_prefix + lib.constants.m_result_logs_delimiter +"*"+ args.id +"*"))
    for f in files_to_open:
      fd = open(f,"r")
      data = simplejson.loads(fd.read())
      fd.close()
      print("\n")
      print(simplejson.dumps(data,indent=4))

  if(args.clean):
    try:
      lib.db_sqlite3.execute("delete from log",
                             db_file=lib.constants.m_dostates_sqlite3_file)

      host_details = glob.glob(os.path.join(lib.constants.m_result_logs_dir, lib.constants.m_result_logs_prefix_hosts + lib.constants.m_result_logs_delimiter + "*"))
      logs = glob.glob(os.path.join(lib.constants.m_result_logs_dir, lib.constants.m_result_logs_prefix + lib.constants.m_result_logs_delimiter + "*"))
      for hd in host_details:
        os.remove(hd)
      for lg in logs:
        os.remove(lg)

    except:
      print(sys.exc_info())


