# bot/cogs/echo.py

# LIBRARIES AND MODULES

## pycord

import discord
from discord.ext import commands

## pypkg

from bot.constants import *
import bot.console as console
import bot.utils as utils

# CLASSES

class Echo(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  async def _echo(self, ctx, msg=None, is_slash=False):
    user = ctx.author

    console.log(f"{user} requested an echo.", "LOG")

    if msg is None:
      console.log("There is nothing to echo, returning.", "INFO")
      await utils.say(ctx, "There's nothing to echo.", is_slash=True, ephemeral=True)
      return
    
    console.log(f"To be echoed: {msg}", "INFO")
    await utils.say(ctx, msg, is_slash=is_slash)
  
  # prefix command
  @commands.command()
  async def echo(self, ctx: commands.Context, *, msg=None):
    await self._echo(ctx, msg)
  
  # slash command
  @commands.slash_command(name="echo", description="make the bot say something!")
  @discord.option("message", description="what to say", type=str)
  async def slash_echo(self, ctx: discord.ApplicationContext, msg=None):
    await self._echo(ctx, msg, is_slash=True)

# FUNCTIONS

def setup(bot):
  bot.add_cog(Echo(bot))