# bot/constants.py

# LIBRARIES AND MODULES

try:
  from colorama import init, Fore, Style
  no_color = False
except ImportError:
  no_color = True

from dotenv import load_dotenv
from pathlib import Path
import os

# CONSTANTS

# usually in a constants file you don't see any function calls
# but the try-except down there is a necessary evil and exception
# to that rule.

env_path = Path(".env")

if not env_path.exists():
  env_prefix = None
else:
  load_dotenv(dotenv_path=env_path)
  env_prefix = os.getenv("PREFIX")

default_prefix = "."
prefix = default_prefix if env_prefix is None else env_prefix

# EXTENSIONS

extensions = (
  # fun fact: i tried to use pathlib for this.
  #           i immediately had an aneurysm trying to understand
  #           HOW to implement it.
  #           so yeah, ig we hardcoding now. deal with it.
  
  "bot.cogs.ping",
  "bot.cogs.help",
  "bot.cogs.echo",
  "bot.cogs.invite",
  "bot.cogs.moderation.ban",
  "bot.cogs.moderation.kick",
  "bot.cogs.moderation.timeout"
)

# CONSOLE

if not no_color:
  init()
  reset_colors = Style.RESET_ALL
else:
  reset_colors = ''

log_colors = {
  "LOG": Fore.WHITE if not no_color else '',
  "DEBUG": Fore.CYAN if not no_color else '',
  "INFO": Fore.BLUE if not no_color else '',
  "WARN": Fore.YELLOW if not no_color else '',
  "ERROR": Fore.RED if not no_color else '',
  "FATAL": (Fore.RED + Style.BRIGHT) if not no_color else ''
}
