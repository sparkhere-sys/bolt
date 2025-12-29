#!/usr/bin/env python3
# bot/utils.py
'''
common utilities used throughout the bot's codebase

essentially,
just a group of functions that don't belong anywhere else,
because DRY.
'''

# LIBRARIES AND MODULES

from typing import Any
from dotenv import load_dotenv
import os

## pycord

import discord
from discord.ext import commands

## pypkg

from bot.constants.config import env_path, units

# FUNCTIONS

def get_env_var(var: str, default: Any, required=True, from_dot_env=True):
  '''
  literally does what it says on the tin
  why does this need a docstring
  NOTE: we are soon to be moving to a TOML config system.
        the .env file however will remain for the token and other secrets,
        so this function will be rewritten to be extremely simple.
  '''
  
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

def parse_duration(duration: str): # the return type annotations are gone now. screw you.
  '''
  parses a value like "1h30m" into seconds.
  returns None if the duration is empty (or 0)
  and returns False if the duration is invalid.

  we're NOT using regex for this.
  spark says "regex makes me have an aneurysm."
  '''

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

async def say(ctx: discord.ApplicationContext | commands.Context, msg: str, ephemeral=False):
  '''
  a wrapper around ctx.send() and ctx.respond().
  '''

  if isinstance(ctx, discord.ApplicationContext):
    await ctx.respond(msg, ephemeral=ephemeral)
  else:
    await ctx.send(msg)

async def assert_guild(ctx):
  # spark: i despise this function

  return ctx.guild is not None
