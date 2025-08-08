# bot/cogs/help.py
# TODO: add docstrings

# LIBRARIES AND MODULES

## pycord

import discord
from discord.ext import commands

## pypkg

import bot.console as console
from bot.constants import *
import bot.utils as utils

# CLASSES

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def _help(self, ctx, is_slash=False):
    user = ctx.author

    console.log(f"Help requested by {user} ({user.id})", "LOG")

    # use markdown for that
    message = f"""
## Available Commands

### Uncategorized

`{prefix}help`: This message
`{prefix}ping`: Ping the bot.
`{prefix}echo`: Make the bot say something.

### Moderation

`{prefix}ban`: Ban a member.
`{prefix}kick`: Kick a member.
`{prefix}mute`: Mute a member.
`{prefix}unmute`: Unmute a member.

## Support Server
Join the support server:
https://discord.gg/hF6mgCE3gT

Bolt is open source! You can find the code at https://github.com/sparkhere-sys/bolt
"""
    
    await utils.say(ctx, message, is_slash=is_slash)

  # prefix command
  @commands.command()
  async def help(self, ctx: commands.Context):
    await self.send_message(ctx)

  # slash commands
  @commands.slash_command(name="help", description="send the help message.")
  async def slash_help(self, ctx: discord.ApplicationContext):
    await self.send_message(ctx, is_slash=True)

# FUNCTIONS

def setup(bot):
  bot.add_cog(Help(bot))
