#!/usr/bin/env python3

# IMPORTS

import time
from typing import Any
from pathlib import Path
from traceback import format_exc

## bolt

from bot.constants.colors import LogLevel, dim, reset
import bot.constants.toml as toml_config

# FUNCTIONS

def format_msg(msg: Any, level: LogLevel) -> None:
  log_dir = Path("logs")
  log_dir.mkdir(exist_ok=True)

  log_file = log_dir / f"{time.strftime('%Y-%m-%d')}.log"
  
  if level.name in toml_config.levels_to_ignore:
    return

  level_str = level.badge
  time_str = f"{dim}{time.asctime(time.localtime())}{reset}"

  level_str_plain = level.plain_badge
  time_str_plain = f"{time.asctime(time.localtime())}"

  full = f"{level_str} {time_str} {msg}"
  full_plain = f"{level_str_plain} {time_str_plain} {msg}"

  print(full)

  with log_file.open("a", encoding="utf-8") as file:
    file.write(full_plain + "\n")

def log(msg: Any) -> None:
  format_msg(msg, LogLevel.LOG)

def debug(msg: Any) -> None:
  format_msg(msg, LogLevel.DEBUG)

def error(msg: Any) -> None:
  format_msg(msg, LogLevel.ERROR)

def fatal(msg: Any) -> None:
  format_msg(msg, LogLevel.FATAL)

def error_traceback() -> None:
  format_msg(format_exc(), LogLevel.ERROR) # your eyes do not deceive you.

def warn(msg: Any) -> None:
  format_msg(msg, LogLevel.WARN)

def info(msg: Any) -> None:
  format_msg(msg, LogLevel.INFO)

def success(msg: Any) -> None:
  format_msg(msg, LogLevel.SUCCESS)