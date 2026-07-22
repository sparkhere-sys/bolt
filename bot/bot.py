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
from bot.constants.colors import LogLevel

# INIT

token = utils.get_env_var("TOKEN", default=None, required=True, from_dot_env=True)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=toml_config.prefix, intents=intents, help_command=None) # create bot instance, remove built-in help command

# FUNCTIONS

## EVENTS

@bot.event
async def on_ready():
  setattr(bot, "start_time", time.time())
  console.translate(f"Bolt is online as {bot.user}", LogLevel.READY)

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
        console.debug(f"Reloaded extension: {ext}")
        continue

      bot.load_extension(ext)
      console.debug(f"Loaded extension: {ext}")
    except Exception as e:
      console.error(f"Failed to load extension: {ext}")
      console.debug(f"Exception: {e}")
      if reraise:
        raise

def start_bot():
  load_cogs()
  bot.run(token)
