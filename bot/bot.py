#!/usr/bin/env python3
# bot/bot.py
'''
Bootstrapper for the bot.

Initializes the bot, loads cogs, and starts the bot.
'''

# LIBRARIES AND MODULES

import time

## pycord

import discord
from discord.ext import commands

## pypkg

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
  '''
  This function is an event that runs when the bot is ready.

  Sets the bot's start time and logs that the bot is online.

  ### Parameters
  none

  ### Returns
  nothing.

  ### Raises
  nothing.
  '''

  setattr(bot, "start_time", time.time())
  console.translate(f"Bolt is online as {bot.user}", LogLevel.READY)

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
  '''
  This function is an event that runs on every command error.

  This currently only handles CommandNotFound errors, as the cogs are expected to have their own
  error handling.

  ### Parameters
  * ctx (commands.Context): the context of the command that caused the error.
                            only handles prefix commands, not slash commands.
  * error (commands.CommandError): the error that was raised

  ### Returns
  nothing.

  ### Raises
  nothing.
  '''

  if isinstance(error, commands.CommandNotFound):
    console.error(str(error))
    await utils.say(ctx, f"Command not found. \nRun {toml_config.prefix}help to see all available commands.")

## START UP

def load_cogs(reload=False, reraise=True):
  '''
  This function loads all cogs defined in constants.extensions.

  ### Parameters
  * reload (bool): whether to reload the cogs instead of loading them. default: False
  * reraise (bool): whether to reraise exceptions encountered while loading cogs. default: True

  ### Returns
  nothing.

  ### Raises
  No specific exceptions, but will reraise any exceptions encountered while loading cogs if reraise is True.
  '''

  for ext in constants.extensions:
    try:
      if reload:
        bot.reload_extension(ext)
        console.debug(f"Reloaded extension: {ext}")
        return

      bot.load_extension(ext)
      console.debug(f"Loaded extension: {ext}")
    except Exception as e:
      console.error(f"Failed to load extension: {ext}")
      console.debug(f"Exception: {e}")
      if reraise:
        raise

def start_bot():
  '''
  This function starts the bot.

  ### Parameters
  none.

  ### Returns
  nothing.

  ### Raises
  nothing.
  '''
  # okay dude did this seriously need a docstring
  # if you needed a docstring to comprehend how this works then you my friend
  # lack basic mental abilities. -spark

  load_cogs()
  bot.run(token)
