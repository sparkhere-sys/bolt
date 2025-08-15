# bot/bot.py
# TODO: add docstrings

# LIBRARIES AND MODULES

from pathlib import Path

## pycord

import discord
from discord.ext import commands

## pypkg

from bot.constants import *
import bot.console as console
import bot.utils as utils

# INIT

token = utils.get_env_var("TOKEN", default=None, required=True, from_dot_env=True) # get token

intents = discord.Intents.default()
intents.message_content = True
# if reaction roles will be added to the bot, then intents.reactions = True

bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None) # create bot instance, remove built-in help command

# FUNCTIONS

@bot.event
async def on_ready():
  console.log(f"Bolt is online as {bot.user}", "LOG")

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    console.log(str(error), "ERROR")
    await utils.say(ctx, f"Command not found. \nRun {prefix}help to see all available commands.") # is_slash is False by default

## START UP

def load_cogs():
  for ext in extensions:
    try:
      bot.load_extension(ext)
      console.log(f"Loaded extension: {ext}", "DEBUG")
    except Exception as e:
      console.log(f"Failed to load extension: {ext}", "DEBUG")
      console.log(f"Exception: {e}", "DEBUG")
      raise

def run():
  load_cogs()
  bot.run(token)