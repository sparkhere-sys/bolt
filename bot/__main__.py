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

    reraise = True

    if "--ignore-startup-errors" in sys.argv:
      reraise = False

    bot.start_bot(reraise)

  except Exception as e:
    console.error(f"Something went wrong. exception: {e}")

# START UP

if __name__ == "__main__":
  main()