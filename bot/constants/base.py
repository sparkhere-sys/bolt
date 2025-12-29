#!/usr/bin/env python3
# bot/constants/base.py
'''
the base constant file that is required for the bot to boot.
contains the bot prefix and the extensions to load.
'''

# LIBRARIES AND MODULES

from pathlib import Path
import re # I HATE REGEX -spark

## pypkg

from bot.utils import get_env_var
from bot.constants.config import default_prefix

# CONSTANTS

prefix = get_env_var("PREFIX", default=default_prefix, required=False, from_dot_env=True) 
# NOTE: the above line will be removed soon and replaced by toml config system

# ad: this feels very cursed
# spark: it 100% is.

_cogs = list(Path('bot/cogs').iterdir())
extensions = []
_regex = lambda i : re.sub('[/\\\\]', '.', re.sub('.py$','',str(i.relative_to('bot/cogs'))))
_ignored_files = ('__pycache__', '__init__.py', 'base.py')

for i in _cogs:
  if i.name in _ignored_files:
    continue

  if i.is_file():
    extensions.append(f"bot.cogs.{_regex(i)}")
  else:
    for j in i.iterdir():
      _cogs.append(j)