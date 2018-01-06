#!/usr/bin/python3

from sys import argv, exit

backlight_dir = '/sys/class/backlight/intel_backlight'
br_steps = [0, 1, 200, 500, 1000, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000, 19200]
max_brightness = 19200


class StepSelect:
  def __init__(self, steps):
    self.steps = steps

  def get_next_step(self, x):
    for i in range(0, len(self.steps)):
      if self.steps[i] > x:
        return self.steps[i]
    return max(self.steps)

  def get_prev_step(self, x):
    for i in range(1, len(self.steps)):
      if self.steps[i] >= x:
        return self.steps[i - 1]
    return min(self.steps)


class Backlight:
  def __init__(self, bdir: str, maxbr = None):
    self.brightness_file = bdir + "/brightness"
    self.max_brightness_file = bdir + "/max_brightness"
    self.brightness = None
    self.maxBrightness = maxbr

  def update_brightness(self):
    with open(self.brightness_file, "r") as br:
      self.brightness = int(br.readline())

  def get_max_brightness(self) -> int:
    if self.maxBrightness is None:
      with open(self.brightness_file, "r") as mbr:
        self.maxBrightness = int(mbr.readline())
    return self.maxBrightness

  def get_brightness(self) -> int:
    if self.brightness is None:
      self.update_brightness()
    return self.brightness

  def set_brightness(self, b):
    with open(self.brightness_file, "w") as br:
      br.write(str(b))


if __name__ == "__main__":
  bl = Backlight(backlight_dir, max_brightness)
  step = StepSelect(br_steps)

  direction = None
  distance = None

  if len(argv) <= 1:
    print(bl.get_brightness())
    exit(0)
  else:
    direction = argv[1]
    if direction != '+' and direction != '-':
      print("Please use + or - as the first argument only.")
    if len(argv) > 2:
      try:
        distance = int(argv[2])
      except ValueError:
        print("Please supply a number as the second argument")
        exit(1)

  if distance is not None:
    if direction == '-':
      distance = -distance
    bl.set_brightness(bl.get_brightness() + int(distance))
    exit(0)

  if direction == '+':
    bl.set_brightness(step.get_next_step(bl.get_brightness()))
  if direction == '-':
    bl.set_brightness(step.get_prev_step(bl.get_brightness()))
