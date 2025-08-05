# bot/console.py

# LIBRARIES AND MODULES

import time

# FUNCTIONS

def log(msg, type_):
  print(f"[{type_.upper()}] [{time.asctime(time.gmtime())}] {msg}")