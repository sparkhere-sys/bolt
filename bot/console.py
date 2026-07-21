#!/usr/bin/env python3

# LIBRARIES AND MODULES

import time # TODO: replace with datetime maybe
from typing import Any

## pypkg

from bot.constants.colors import LogLevel
import bot.constants.toml as toml_config

# FUNCTIONS

def translate(msg: Any, level: LogLevel) -> None:
  if level.name in toml_config.levels_to_ignore:
    return

  level_str = level.badge
  time_str = time.asctime(time.localtime())

  full = f"{level_str} {time_str} {msg}"

  print(full)

def log(msg: Any, _backwards_compatibility=None) -> None:
  translate(msg, LogLevel.LOG)

def debug(msg: Any, _backwards_compatibility=None) -> None:
  translate(msg, LogLevel.DEBUG)

def error(msg: Any, _backwards_compatibility=None) -> None:
  translate(msg, LogLevel.ERROR)

def fatal(msg: Any, _backwards_compatibility=None) -> None:
  translate(msg, LogLevel.FATAL)

def warn(msg: Any, _backwards_compatibility=None) -> None:
  translate(msg, LogLevel.WARN)

def info(msg: Any, _backwards_compatibility=None) -> None:
  translate(msg, LogLevel.INFO)