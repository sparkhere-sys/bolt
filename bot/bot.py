# bot/bot.py
# TODO: add docstrings

# LIBRARIES AND MODULES

import os
from dotenv import load_dotenv
from pathlib import Path

## pycord

import discord
from discord.ext import commands

## pypkg

from bot.constants import *
import bot.console as console
import bot.utils as utils

# LOAD .env FILE

if not env_path.exists(): # env_path is in constants.py
  console.log("No .env file found.", "FATAL")
  raise FileNotFoundError("fatal: No .env file found, please create one including your bot's token.")

load_dotenv(dotenv_path=env_path)
token = os.getenv("TOKEN")

if token is None:
  console.log("No Discord token found.", "FATAL")
  raise ValueError("fatal: No Discord token found.")

# INIT

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command("help") # remove the built-in help command

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