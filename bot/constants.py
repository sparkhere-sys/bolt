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
  "bot.cogs.ping",
  "bot.cogs.help",
  "bot.cogs.moderation.ban",
  "bot.cogs.moderation.kick"
)

# CONSOLE

if not no_color:
  init()

log_colors = {
  "LOG": Fore.WHITE if not no_color else '',
  "INFO": Fore.BLUE if not no_color else '',
  "ERROR": Fore.YELLOW if not no_color else '',
  "FATAL": Fore.RED if not no_color else ''
}

reset_colors = Style.RESET_ALL