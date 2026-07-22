#!/usr/bin/env python3

# IMPORTS

import time # TODO: replace with datetime maybe
from typing import Any

## bolt

from bot.constants.colors import LogLevel, dim, reset
import bot.constants.toml as toml_config

# FUNCTIONS

def translate(msg: Any, level: LogLevel) -> None:
  if level.name in toml_config.levels_to_ignore:
    return

  level_str = level.badge
  time_str = f"{dim}{time.asctime(time.localtime())}{reset}"

  full = f"{level_str} {time_str} {msg}"

  print(full)

def log(msg: Any) -> None:
  translate(msg, LogLevel.LOG)

def debug(msg: Any) -> None:
  translate(msg, LogLevel.DEBUG)

def error(msg: Any) -> None:
  translate(msg, LogLevel.ERROR)

def fatal(msg: Any) -> None:
  translate(msg, LogLevel.FATAL)

def warn(msg: Any) -> None:
  translate(msg, LogLevel.WARN)

def info(msg: Any) -> None:
  translate(msg, LogLevel.INFO)