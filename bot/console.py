# bot/console.py

# LIBRARIES AND MODULES

import time

## pypkg

## from bot.constants import *
from bot.constants import log_colors, reset_colors # even though we used to have a * import, 
                                                   # we have to lazy import those two variables
                                                   # for some godforsaken reason

# FUNCTIONS

def log(msg, level="LOG"):
  # why the hell did i have to add a lazy import
  # screw you python.

  print(f"{log_colors[level.upper()]}[{level.upper()}]{reset_colors} [{time.asctime(time.gmtime())}] {msg}")
  # in plain english,
  # it just outputs:
  # [LOG] [current time] [message]
