# bot/bot.py
# TODO: add docstrings

# LIBRARIES AND MODULES

import os
from dotenv import load_dotenv

## pycord

import discord
from discord.ext import commands

## pypkg

from bot.constants import *
import bot.console as console

# LOAD .env FILE

load_dotenv()
token = os.getenv("TOKEN")

if token is None:
  console.log("No Discord token found.", "FATAL")
  raise ValueError("fatal: No Discord token found.")

# INIT

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents)

# FUNCTIONS

@bot.event
async def on_ready():
  console.log(f"Bolt is online as {bot.user}", "LOG")

def load_cogs():
  bot.load_extension("bot.cogs.ping")

def run():
  load_cogs()
  bot.run(token)