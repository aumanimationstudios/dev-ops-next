#!/usr/bin/env python3
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import socket
import time
sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.constants
import lib.config


if 'id' in lib.config.slave_conf:
  hostname = lib.config.slave_conf['id']
  ip = "0.0.0.0"
else:
  retry_count = 3
  hostname = socket.gethostname()
  hostname_count = 0
  while hostname.find("localhost") >= 0:
    if hostname_count >= retry_count:
      raise Exception("hostname not found. please provide an id in the slave.conf file")
    time.sleep(1)
    hostname = socket.gethostname()
    hostname_count = hostname_count + 1

  try:
    ip = socket.gethostbyname(hostname)
  except Exception as e:
    raise Exception("ip not found. please provide an id in the slave.conf file") from e
