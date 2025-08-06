# bot/__main__.py

import bot.bot as bot
import bot.console as console

if __name__ == "__main__":
  try:
    console.log("Starting Bolt...", "LOG")
    bot.run()
  except Exception as e:
    console.log(f"Something happened. exception: {e}", "FATAL")