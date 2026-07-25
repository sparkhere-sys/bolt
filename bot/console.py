#!/usr/bin/env python3

# IMPORTS

import time # TODO: replace with datetime maybe
from typing import Any

## bolt

from bot.constants.colors import LogLevel, dim, reset
import bot.constants.toml as toml_config

# FUNCTIONS

def format_msg(msg: Any, level: LogLevel) -> None:
  if level.name in toml_config.levels_to_ignore:
    return

  level_str = level.badge
  time_str = f"{dim}{time.asctime(time.localtime())}{reset}"

  full = f"{level_str} {time_str} {msg}"

  print(full)

def log(msg: Any) -> None:
  format_msg(msg, LogLevel.LOG)

def debug(msg: Any) -> None:
  format_msg(msg, LogLevel.DEBUG)

def error(msg: Any) -> None:
  format_msg(msg, LogLevel.ERROR)

def fatal(msg: Any) -> None:
  format_msg(msg, LogLevel.FATAL)

def warn(msg: Any) -> None:
  format_msg(msg, LogLevel.WARN)

def info(msg: Any) -> None:
  format_msg(msg, LogLevel.INFO)

def success(msg: Any) -> None:
  format_msg(msg, LogLevel.SUCCESS)