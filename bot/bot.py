#!/usr/bin/env python3
# bot/bot.py

# IMPORTS

import time

## pycord

import discord
from discord.ext import commands

## bolt

import bot.constants.base as constants
import bot.constants.toml as toml_config
import bot.console as console
import bot.utils as utils

# INIT

token = utils.get_env_var("TOKEN", default=None, required=True, from_dot_env=True)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=toml_config.prefix, intents=intents, help_command=None) # we remove the built-in help command

# FUNCTIONS

## EVENTS

@bot.event
async def on_ready():
  setattr(bot, "start_time", time.time()) # mind your own damn business, pylance
  console.success(f"Bolt is online as {bot.user}")

@bot.event
async def on_disconnect():
  console.warn("Disconnected from Discord.")

@bot.event
async def on_resumed():
  console.log("Resumed connection to Discord.")

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
  if isinstance(error, commands.CommandNotFound):
    console.error(str(error))
    await utils.say(ctx, f"Command not found. \nRun {toml_config.prefix}help to see all available commands.")

## START UP

def load_cogs(reload=False, reraise=True):
  for ext in constants.extensions:
    try:
      if reload:
        bot.reload_extension(ext)
        console.info(f"Reloaded extension: {ext}")
        continue

      bot.load_extension(ext)
      console.info(f"Loaded extension: {ext}")
    except Exception:
      console.error(f"Failed to load extension: {ext}")
      console.error_traceback()
      if reraise: # in this case, we're printing the traceback
                  # without needing to reraise, so technically
                  # this just means abort if any extension 
                  # fails to load
        return

def start_bot(reraise=True):
  load_cogs(reraise=reraise)
  bot.run(token)
