#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import os
import sys

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.config
import lib.constants
import lib.debug
import lib.hostname_ip
if os.path.exists(lib.constants.s_slaveconst_dir):
  sys.path.append(lib.constants.s_slaveconst_dir)

import glob
import platform
import distro
import hashlib


class slaveconst(object):
  def __init__(self):
    self.__retdict = self.__get_preset_consts()
    self.__userconst = self.__update_slaveconst()
    self.__retdict.update(self.__userconst)

  def slaveconst(self):
    lib.debug.debug(self.__retdict)
    return(self.__retdict)

  def __get_preset_consts(self):
    retdict = {}
    retdict['hostname'] = lib.hostname_ip.hostname
    retdict['ip'] = lib.hostname_ip.ip
    retdict['platform'] = platform.system()
    retdict['architecture'] = platform.architecture()
    # retdict['os'] = platform.dist()
    # retdict['os'] = '_'.join(os.uname().release.split('.')[0:2])
    retdict['os'] = (distro.name(), os.uname().release.split('-')[0], distro.id())
    retdict['id'] = hostid()
    try:
      retdict['slave_group'] = lib.config.slave_conf['slave_group'].split(",")
    except:
      retdict['slave_group'] = "slave"
    return retdict

  def __update_slaveconst(self):
    userconsts = {}
    if os.path.exists(lib.constants.s_slaveconst_dir):
      pyfiles = glob.glob(os.path.join(lib.constants.s_slaveconst_dir, "*.py"))
      if pyfiles:
        for x in pyfiles:
          module_to_load = ".".join(x.split(os.sep)[-1].split(".")[:-1])
          module_consts = {}
          exec("import " + module_to_load)
          exec("module_consts = " + module_to_load + ".update_consts()")
          if module_consts:
            userconsts.update(module_consts)
          del module_to_load

    return userconsts


def hostid():
  if 'id' in lib.config.slave_conf:
    return lib.config.slave_conf['id']
  else:
    return lib.hostname_ip.hostname


if __name__ == '__main__':
  consts = slaveconst()
  print(consts.slaveconst())
  print(hostid())

