#!/usr/bin/env python3
# bot/__main__.py
'''
Main entry point for the bot.

Runs when executing `python -m bot`.
'''

# LIBRARIES AND MODULES

## pypkg

from bot.constants.colors import allow_colors
import bot.bot as bot
import bot.console as console

# FUNCTIONS

def main():
  '''
  The bootstrapper.

  ### Parameters
  none.

  ### Returns
  nothing.

  ### Raises
  nothing.
  '''
  
  try:
    console.log("Starting Bolt...")

    if not allow_colors:
      console.log("You don't have `colorama` installed. If you want colored logs, run `pip install colorama`.")

    bot.start_bot()

  except Exception as e:
    console.log(f"Something happened. exception: {e}")

  except KeyboardInterrupt:
    console.log(f"Bolt shutting down...")

# START UP

if __name__ == "__main__":
  main()