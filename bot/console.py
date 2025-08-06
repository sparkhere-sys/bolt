# bot/console.py

# LIBRARIES AND MODULES

import time

## pypkg

from bot.constants import *

# FUNCTIONS

def log(msg, type_="LOG"):
  print(f"{log_colors[type_.upper()]}[{type_.upper()}]{reset_colors} [{time.asctime(time.gmtime())}] {msg}")
  # in plain english,
  # it just outputs:
  # [LOG] [current time] [message]
