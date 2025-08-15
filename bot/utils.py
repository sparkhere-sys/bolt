# bot/utils.py

# LIBRARIES AND MODULES

from dotenv import load_dotenv
import os

## pycord

import discord
from discord.ext import commands

## pypkg

import bot.console as console
from bot.constants import *

# FUNCTIONS

def get_env_var(var, default, required=True, from_dot_env=True):
  if from_dot_env:
    if not env_path.exists():
      console.log(f"No .env file found.", "WARN" if not required else "FATAL")
      if required:
        raise FileNotFoundError(f"fatal: No .env file found, please create one including {var}")
      else:
        console.log(f"Using default value for {var}: {default}", "DEBUG")
        return default
    
    load_dotenv(dotenv_path=env_path)

  val = os.getenv(var, default)
  if val is None and required:
    console.log(f"Required variable ({var}) not found in .env file.", "FATAL")
    raise ValueError(f"fatal: Required variable ({var}) not found in .env file.")
    
  return val

async def say(ctx: discord.ApplicationContext | commands.Context, msg: str, is_slash=False, ephemeral=False):
  if is_slash:
    await ctx.respond(msg, ephemeral=ephemeral)
  else:
    await ctx.send(msg)

async def assert_guild(ctx, guild, user, is_slash=False):
  if guild is None:
    console.log(f"{user} tried to run a command where it's not supported.", "LOG")
    await say(ctx, "You can't run that command here!", is_slash=is_slash, ephemeral=True)
    return False
  
  return True
