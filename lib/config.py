#!/usr/bin/env python3
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import os
import sys
sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

import lib.constants
import yaml

slave_conf = {}
master_conf = {}

if os.path.exists(lib.constants.s_config_file):
  with open(lib.constants.s_config_file, "r") as __slave_fd:
    slave_conf = yaml.safe_load(__slave_fd)

if os.path.exists(lib.constants.m_config_file):
  with open(lib.constants.m_config_file, "r") as __master_fd:
    master_conf = yaml.safe_load(__master_fd)
