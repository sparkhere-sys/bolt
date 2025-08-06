# bot/cogs/echo.py

# LIBRARIES AND MODULES

## pycord

import discord
from discord.ext import commands

## pypkg

from bot.constants import *
import bot.console as console

# CLASSES

class Echo(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  async def echo_message(self, ctx: commands.Context, msg=None, is_slash=False):
    user = ctx.author
    console.log(f"{user} requested an echo.", "LOG")

    if msg is None:
      console.log("There is nothing to echo, returning.", "INFO")
      if is_slash:
        await ctx.respond("There's nothing to echo.")
      else:
        await ctx.send("There's nothing to echo.")
      return
    
    console.log(f"To be echoed: {msg}", "INFO")

    if is_slash:
      await ctx.respond(msg)
    else:
      await ctx.send(msg)
  
  # prefix command
  @commands.command()
  async def echo(self, ctx: commands.Context, msg=None):
    await self.echo_message(ctx, msg)
  
  # slash command
  @commands.slash_command(name="echo", description="make the bot say something!")
  @discord.option("what to say", type=str)
  async def slash_echo(self, ctx: discord.ApplicationContext, msg=None):
    await self.echo_message(ctx, msg, is_slash=True)

# FUNCTIONS

def setup(bot):
  bot.add_cog(Echo(bot))