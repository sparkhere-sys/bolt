# bot/constants.py

# LIBRARIES AND MODULES

try:
  from colorama import init, Fore, Style
  no_color = False
except ImportError:
  no_color = True

from dotenv import load_dotenv
import os

# CONSTANTS

# usually in a constants file you don't see any function calls
# but the try-except down there is a necessary evil and exception
# to that rule.

try:
  load_dotenv()
  env_prefix = os.getenv("PREFIX")
except FileNotFoundError:
  env_prefix = None

default_prefix = "."
prefix = default_prefix if env_prefix is None else env_prefix

# EXTENSIONS

extensions = (
  # TODO: use pathlib and iterdir for this
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
