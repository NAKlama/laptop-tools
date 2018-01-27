#!/usr/bin/python3

import os.path as path
import subprocess
import re
import yaml
try:
  from yaml import CLoader as YamlLoader, CDumper as YamlDumper
except ImportError:
  from yaml import Loader as YamlLoader, Dumper as YamlDumpetr
from typing import List

#
# BEGIN: Global Variables for individual setups
#
configFile = "~/.screen-switcher.yaml"
#
# END: Global Variables for individual setups
#

configFile = path.abspath(path.expanduser(configFile))
default_config = { 'xrandr':      "xrandr"
                 , 'current':     0
                 , 'screens':     []
                 , 'config':      []
                 }


class Xrandr:
  def __init__(self, prog: str, config_in: List[List[List[str]]]):
    self.xrandr         = prog
    self.activeScreens  = []
    self.config         = config_in

    ret = subprocess.run([self.xrandr], stdout=subprocess.PIPE)
    out = ret.stdout.decode('utf-8').split('\n')
    for l in out:
      match = re.match(r'^(\w*) connected.*$', l)
      if match:
        self.activeScreens.append(match.group(1))

  def switch(self, num: int):
    if num >= len(self.config):
      raise OverflowError
    this_conf = self.config[num]
    for group in this_conf:
      keyword, master, *screens = group
      subprocess.run([self.xrandr, "--output", master, "--auto"])
      if keyword == "mirror":
        for s in screens:
          subprocess.run([self.xrandr, "--output", s, "--auto", "--same-as", master])
      elif keyword == "right":
        for s in screens:
          subprocess.run([self.xrandr, "--output", s, "--auto", "--right-of", master])
          master = s
      elif keyword == "left":
        for s in screens:
          subprocess.run([self.xrandr, "--output", s, "--auto", "--left-of", master])
          master = s
      elif keyword == "off" or not keyword:
        subprocess.run([self.xrandr, "--output", master, "--off"])
        for s in screens:
          subprocess.run([self.xrandr, "--output", s, "--off"])
      elif keyword == "on" or keyword:
        for s in screens:
          subprocess.run([self.xrandr, "--output", s, "--auto"])


if __name__ == "__main__":
  if path.exists(configFile) and path.isfile(configFile):
    with open(configFile, "r") as conf:
      config = yaml.load(conf, Loader=YamlLoader)
  else:
    config = default_config

  Xr  = Xrandr(config['xrandr'], config['config'])

  for screen in Xr.activeScreens:
    if screen not in config['screens']:
      config['screens'].append(screen)

  if config['current']+1 >= len(config['config']):
    config['current'] = 0
  else:
    config['current'] += 1

  Xr.switch(config['current'])

  with open(configFile, "w") as conf:
    yaml.dump(config, conf, Dumper=YamlDumper)
