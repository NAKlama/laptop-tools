#!/usr/bin/python3

from sys import argv, exit

backlight_dir = "/sys/class/backlight/intel_backlight"
br_steps = [0, 1, 200, 500, 1000, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000, 19200]
max_brightness = 19200


class StepSelect:
  def __init__(self, steps):
    self.steps = steps

  def getNextStep(self, x):
    for i in range(0, len(self.steps)):
      if (self.steps[i] > x):
        return self.steps[i]
    return max(self.steps)

  def getPrevStep(self, x):
    for i in range(1, len(self.steps)):
      if (self.steps[i] >= x):
        return self.steps[i - 1]
    return min(self.steps)


class Backlight:
  def __init__(self, bDir: str, maxBr: object = int):
    self.brightness_file = bDir + "/brightness"
    self.max_brightnessi_file = bDir + "/max_brightness"
    self.brightness = None
    self.maxBrightness = maxBr

  def updateBrightness(self):
    with open(brightness_file, "r") as br:
      self.brightness = int(br.readline())

  @property
  def getMaxBrightness(self):
    if self.maxBrightness is None:
      with open(brightness_file, "r") as mbr:
        self.maxBrightness = int(mbr.readline())
    return self.maxBrightness

  @property
  def getBrightness(self):
    if self.brightness is None:
      self.updateBrightness()
    return self.brightness

  def setBrightness(self, b):
    with open(self.brightness_file, "r"):
      br.write(b)


bl   = Backlight(backlight_dir, max_brightness)
step = StepSelect(br_steps)

direction = None
distance = None

if (len(argv) <= 1):
  # Maybe add percentage here
  exit(0)
else:
  direction = argv[1]
  if (len(argv) > 2):
    distance = argv[2]

if(distance is not None):
  if(direction == '-'):
    distance = -distance
  bl.setBrightness(bl.getBrightness + int(distance))

if(direction == '+'):
  bl.setBrightness(step.getNextStep(bl.getBrightness))
if(direction == '-'):
  bl.setBrightness(step.getPrevStep(bl.getBrightness))
