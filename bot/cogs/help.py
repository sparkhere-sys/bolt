# bot/cogs/help.py
# TODO: add docstrings

# LIBRARIES AND MODULES

## pycord

from discord.ext import commands

## pypkg

import bot.console as console
from bot.constants import *

# CLASSES

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  async def send_message(self, ctx):
    user = ctx.author
    
    console.log(f"Help requested by {user} ({user.id})", "LOG")

    _help = f"""
## Available Commands

{prefix}help: This message
{prefix}ping: Ping the bot.

## Support Server
Join the support server:
https://discord.gg/hF6mgCE3gT
"""
    await ctx.send(_help)
  
  # prefix command
  @commands.command()
  async def help(self, ctx):
    await self.send_message(ctx)
  
  # slash commands
  @commands.slash_command(name="help", description="send the help message.")
  async def slash_help(self, ctx):
    await self.send_message(ctx)

# FUNCTIONS
def setup(bot):
  bot.add_cog(Help(bot))