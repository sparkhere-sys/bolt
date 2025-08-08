# bot/cogs/invite.py

# LIBRARIES AND MODULES

## pycord

import discord
from discord.ext import commands

## pypkg

import bot.utils as utils
import bot.console as console

# CLASSES

class Invite(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  async def _invite(self, ctx, is_slash=False):
    user = ctx.author

    message = """
Add Bolt to your server!
https://sparkhere-sys.github.io/bolt

Support server:
https://discord.gg/hF6mgCE3gT
    """

    console.log(f"{user} requested an invite link.", "LOG")
    await utils.say(ctx, message, is_slash=is_slash)
  
  @commands.command()
  async def invite(self, ctx: commands.Context):
    await self._invite(ctx)
  
  @commands.slash_command(name="invite", description="invite the bot to your server!")
  async def slash_invite(self, ctx: discord.ApplicationContext):
    await self._invite(ctx, is_slash=True)

# FUNCTIONS

def setup(bot):
  bot.add_cog(Invite(bot))