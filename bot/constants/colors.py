# bot/constants/colors.py

# LIBRARIES AND MODULES

try:
  from colorama import init, Fore, Style
  _allow_colors = True
  init()
except ImportError:
  _allow_colors = False

# COLORS

log_colors = {
  "LOG": Fore.WHITE if _allow_colors else '',
  "DEBUG": Fore.CYAN if _allow_colors else '',
  "INFO": Fore.BLUE if _allow_colors else '',
  "WARN": Fore.YELLOW if _allow_colors else '',
  "ERROR": Fore.RED if _allow_colors else '',
  "FATAL": (Fore.RED + Style.BRIGHT) if _allow_colors else ''
}

reset_colors = Style.RESET_ALL if _allow_colors else ''