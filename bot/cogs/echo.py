#!/usr/bin/env python3
# bot/cogs/echo.py
'''
Contains the Echo cog.
'''

# LIBRARIES AND MODULES

## pycord

import discord
from discord.ext import commands

## pypkg

import bot.console as console
import bot.utils as utils

# CLASSES

class Echo(commands.Cog):
  '''
  Handles the echo commands.
  '''

  def __init__(self, bot):
    self.bot = bot
  
  async def _echo(self, ctx, msg=None):
    '''
    This function is a bot command.

    Says a message provided by the user in the channel the command was invoked in.

    ### Parameters
    * ctx: discord.ApplicationContext | commands.Context: The context of the command.
    * msg: str | None: The message to echo. If None, informs the user that there's nothing to echo.

    ### Returns
    nothing.

    ### Raises
    nothing.
    '''

    user = ctx.author

    console.log(f"{user} requested an echo.")

    if msg is None:
      console.log("There is nothing to echo, returning.")
      await utils.say(ctx, "There's nothing to echo.", ephemeral=True)
      return
    
    console.log(f"To be echoed: {msg}")
    await utils.say(ctx, msg)
  
  # COMMANDS

  # prefix command
  @commands.command()
  async def echo(self, ctx: commands.Context, *, msg=None):
    await self._echo(ctx, msg)
  
  # slash command
  @commands.slash_command(name="echo", description="make the bot say something!")
  @discord.option("message", description="what to say", type=str)
  async def slash_echo(self, ctx: discord.ApplicationContext, msg=None):
    await self._echo(ctx, msg)

# FUNCTIONS

def setup(bot):
  '''
  Adds the Echo cog to the bot.
  '''

  bot.add_cog(Echo(bot))