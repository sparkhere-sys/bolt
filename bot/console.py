# bot/console.py

# LIBRARIES AND MODULES

import time

## pypkg

## from bot.constants import *
import bot.constants.colors as colors

# FUNCTIONS

def log(msg, level="LOG"):
  print(f"{colors.log_colors[level.upper()]}[{level.upper()}]{colors.reset_colors} [{time.asctime(time.gmtime())}] {msg}")
  # in plain english,
  # it just outputs:
  # [LOG] [current time] [message]
