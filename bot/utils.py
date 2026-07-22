#!/usr/bin/env python3
# bot/utils.py

# IMPORTS

from typing import Any
from dotenv import load_dotenv
import os

## pycord

import discord
from discord.ext import commands

## bolt

from bot.constants.config import env_path, units

# FUNCTIONS

def get_env_var(var: str, default: Any, required=True, from_dot_env=True) -> Any:
  if from_dot_env:
    if not env_path.exists():
      if required:
        raise FileNotFoundError(f"fatal: No .env file found, please create one including {var}")
      else:
        return default

    load_dotenv(dotenv_path=env_path)

  val = os.getenv(var, default)
  if val is None and required:
    raise ValueError(f"fatal: Required variable ({var}) not found in .env file.")

  return val

def parse_duration(duration: str) -> int | bool | None:
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

  return total_seconds if total_seconds > 0 else False

async def say(ctx: commands.Context | discord.ApplicationContext, msg: str = "", ephemeral=False, file:  discord.File | None = None):
  if isinstance(ctx, discord.ApplicationContext):
    if isinstance(file, discord.File):
      await ctx.respond(msg, ephemeral=ephemeral, file=file)
    else:
      await ctx.respond(msg, ephemeral=ephemeral)
  else:
    if isinstance(file, discord.File):
      await ctx.send(msg, file=file)
    else:
      await ctx.send(msg)

async def assert_guild(ctx: commands.Context | discord.ApplicationContext) -> bool:
  # spark: i despise this function
  # it is basically never used

  return ctx.guild is not None
