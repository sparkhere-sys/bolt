#!/usr/bin/env python3
# bot/utils.py

# IMPORTS

from typing import Any, Union
from dotenv import load_dotenv
from os import getenv

## pycord

import discord

## bolt

from bot.constants.config import env_path, units
from bot.constants.types import ContextType

# FUNCTIONS

def get_env_var(var: str, default: Any, required=True, from_dot_env=True) -> Any:
  # NOTE: this function is only ever called once, in bot.py
  #       not sure if this should be deleted since its basically
  #       a vestigial structure of old bolt, but its useful
  
  if from_dot_env:
    if not env_path.exists():
      if required:
        raise FileNotFoundError(f"No .env file found, please create one including {var}")
      else:
        return default

    load_dotenv(env_path)

  val = getenv(var, default)
  if val is None and required:
    raise ValueError(f"Required variable ({var}) not found in .env file.")

  return val

def parse_duration(duration: str, strict=False) -> Union[int, bool, None]:
  # no, we're not using regex. regex makes me have an aneurysm. -spark
  duration = duration.strip().lower()

  if not duration:
    return None

  total_seconds = 0
  num = ''

  for char in duration:
    if char.isdigit():
      num += char
    elif char in units:
      if not num:
        return False # meaning invalid

      total_seconds += int(num) * units[char]
      num = ''
    elif strict: # we use elif because i don't want to nest an if inside an else
                 # this will only run if both `char.isdigit()` and `char in units` are False
      return False

  return total_seconds if total_seconds > 0 else False

async def say(
  ctx: ContextType, 
  msg: str = "", 
  ephemeral=False, 
  file: discord.File | None = None
) -> None:
  if isinstance(ctx, discord.ApplicationContext):
    if isinstance(file, discord.File): # in plain english, if file is not None
      await ctx.respond(msg, ephemeral=ephemeral, file=file)
    else:
      await ctx.respond(msg, ephemeral=ephemeral)
  else:
    if isinstance(file, discord.File):
      await ctx.send(msg, file=file)
    else:
      await ctx.send(msg)
