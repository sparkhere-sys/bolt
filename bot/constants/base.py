#!/usr/bin/env python3
# bot/constants/base.py

# IMPORTS

from pathlib import Path

## bolt

import bot.constants.toml as toml_config

# CONSTANTS

_ignored_files: set[str] = {"__pycache__", "__init__.py", "base.py", "types.py", "case.py"}

extensions = []

for path in Path("bot/cogs").rglob("*.py"):
  if path.name in _ignored_files:
    continue

  module = ".".join(path.relative_to("bot/cogs").with_suffix("").parts)

  if module in toml_config.disabled_cogs:
    continue

  extensions.append(f"bot.cogs.{module}")
