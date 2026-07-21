#!/usr/bin/env python3
# bot/constants/toml.py
'''
Handles loading the config.toml file and loading constants from it.
'''

# LIBRARIES AND MODULES

from pathlib import Path
import tomllib as toml

## pypkg

from bot.constants.config import default_prefix

# PATHS

config_path = Path("config.toml")

# LOAD TOML

try:
  with open(config_path, "rb") as f:
    data = toml.load(f)
except FileNotFoundError:
  data = {}

# CONSTANTS

# could this be cleaner? absolutely. is this the easiest way? also yes.
# ideally this file could use a for-loop structure like constants/base.py but laziness.
# ad if you're reading this please help -spark

preferences = data.get("preferences", {})
logging = data.get("logging", {})
database = data.get("database", {})
cogs = data.get("cogs", {})
markdown = data.get("markdown", {})
log_colors = data.get("log_colors", {})

## preferences

prefix = preferences.get("prefix", default_prefix)
bot_name = preferences.get("bot_name", "Bolt")

## logging

levels_to_ignore = logging.get("levels_to_ignore", [])

## database

# NOTE: not implemented yet

## cogs

disabled_cogs = cogs.get("disabled", [])

## markdown

support_server = markdown.get("support_server", "")
invite_link = markdown.get("invite_link", "")
github_repo = markdown.get("github_repo", "")
help_repo_message = markdown.get("help_repo_message", "")
