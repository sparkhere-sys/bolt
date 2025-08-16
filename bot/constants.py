# bot/constants.py

# LIBRARIES AND MODULES

try:
  from colorama import init, Fore, Style
  no_color = False
except ImportError:
  no_color = True

from pathlib import Path

## pypkg

import bot.utils as utils

# CONSTANTS

env_path = Path(".env")

default_prefix = "."

prefix = utils.get_env_var("PREFIX", default=default_prefix, required=False, from_dot_env=True)

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
