# bot/constants/base.py

# LIBRARIES AND MODULES

## pypkg

from bot.utils import get_env_var
from bot.constants.config import default_prefix

# CONSTANTS

prefix = get_env_var("PREFIX", default=default_prefix, required=False, from_dot_env=True)

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