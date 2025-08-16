# bot/__main__.py

# LIBRARIES AND MODULES

## pypkg

import bot.bot as bot
import bot.console as console

# FUNCTIONS

def main():
  try:
    console.log("Starting Bolt...", "LOG")
    bot.start_bot()
  except Exception as e:
    console.log(f"Something happened. exception: {e}", "FATAL")
  except KeyboardInterrupt:
    console.log(f"Bolt shutting down...", "LOG")

# STARTUP

if __name__ == "__main__":
  main()