#!/usr/bin/env python3
# bot/constants/base.py
'''
Base constant file required for the bot to boot.
'''

# LIBRARIES AND MODULES

from pathlib import Path

## pypkg

import bot.constants.toml as toml_config

# CONSTANTS

_ignored_files = ("__pycache__", "__init__.py", "base.py")

extensions = []

for path in Path("bot/cogs").rglob("*.py"):
  if path.name in _ignored_files:
    continue

  module = ".".join(path.relative_to("bot/cogs").with_suffix("").parts)

  if module in toml_config.disabled_cogs:
    continue

  extensions.append(f"bot.cogs.{module}")
