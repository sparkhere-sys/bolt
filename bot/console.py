# bot/console.py

# LIBRARIES AND MODULES

import time

# FUNCTIONS

def log(msg, type_="LOG"):
  print(f"[{type_.upper()}] [{time.asctime(time.gmtime())}] {msg}")
