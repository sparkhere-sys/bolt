#!/usr/bin/env python3
# bot/__main__.py

# IMPORTS

import sys

## bolt

from bot.constants.colors import allow_colors
import bot.bot as bot
import bot.console as console

# FUNCTIONS

def main():
  try:
    console.log("Starting Bolt...")

    if not allow_colors:
      console.warn("You don't have `colorama` installed. If you want colored logs, run `pip install colorama`.")

    reraise = False

    if "--ignore-startup-errors" in sys.argv:
      reraise = True

    bot.start_bot(reraise)

  except Exception as e:
    console.error(f"Something happened. exception: {e}")
    raise # the traceback is probably the more useful part

# START UP

if __name__ == "__main__":
  main()