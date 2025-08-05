# bot/__main__.py

import bot.bot as bot
import bot.console as console

if __name__ == "__main__":
  try:
    bot.run()
  except Exception as e:
    console.log(f"Something happened. exception: {e}", "FATAL")
  except KeyboardInterrupt:
    console.log("Shutting down...", "LOG")