# bot/constants.py

# LIBRARIES AND MODULES

try:
  from colorama import init, Fore, Style
  no_color = False
except ImportError:
  no_color = True

# CONSTANTS

prefix = "."

# EXTENSIONS

extensions = (
  # TODO: use pathlib and iterdir for this
  "bot.cogs.ping",
  "bot.cogs.help",
  "bot.cogs.echo",
  "bot.cogs.moderation.ban",
  "bot.cogs.moderation.kick"
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
