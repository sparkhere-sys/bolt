# bot/cogs/moderation/kick.py

# LIBRARIES AND MODULES

## pycord

import discord
from discord.ext import commands

## pypkg

from bot.constants import *
import bot.console as console
import bot.utils as utils

# CLASSES

class Kick(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def _kick(self, ctx, member: discord.Member, reason=None, is_slash=False):
    user = ctx.author

    assert ctx.guild

    try:
      if user == member:
        console.log(f"{user} was an idiot and tried to kick themselves.", "LOG")
        await utils.say(ctx, "You can't kick yourself!", is_slash=is_slash, ephemeral=True)
        return
      else:
        console.log(f"{user} Kicked {member} {('for ' + reason) if reason else ''}", "LOG")
        await member.kick(reason=reason or 'None provided.')

    except discord.Forbidden:
      console.log(f"Failed to kick {member}, permission denied.", "ERROR")
      await utils.say(ctx, "I don't have permission to kick that user.", is_slash=is_slash, ephemeral=True)
      return

    except Exception as e:
      console.log(f"Exception raised: {e}", "ERROR")
      await utils.say(ctx, "Something went wrong, try again later.", is_slash=is_slash, ephemeral=True)
      return

    message = f"Kicked {member}. \nReason: {reason or 'None provided.'}"

    await utils.say(ctx, message, is_slash=is_slash)

  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx: commands.Context, member: discord.Member, *, reason=None):
    await self._kick(ctx, member, reason)
  
  @commands.slash_command(name="kick", description="kick a member.")
  @commands.has_permissions(kick_members=True)
  async def slash_kick(self, ctx: discord.ApplicationContext, member: discord.Member, reason=None):
     await self._kick(ctx, member, reason, is_slash=True)

# FUNCTIONS

def setup(bot):
  bot.add_cog(Kick(bot))
