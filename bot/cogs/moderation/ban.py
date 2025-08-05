# bot/cogs/moderation/ban.py

# LIBRARIES AND MODULES

## pycord

import discord
from discord.ext import commands

## pypkg

from bot.constants import *
import bot.console as console

# CLASSES

class Ban(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  def ban_member(self, ctx, member: discord.Member, *, reason: str = None, is_slash=False):
    user = ctx.author

    console.log(f"{user} banned {member} {'for ' + reason if reason else ''}", "LOG")
    try:
      if reason is None:
        member.ban(reason="None provided.")
      else:
        member.ban(reason=reason)
    except discord.Forbidden:
      console.log(f"Failed to ban {member}, permission denied.", "ERROR")
      if is_slash:
        ctx.respond("I don't have permission to ban that user.")
      else:
        ctx.send("I don't have permission to ban that user.")
      
      return False
    except Exception as e:
      console.log(f"Exception raised: {e}", "ERROR")
      if is_slash:
        ctx.send("Something went wrong, try again later.")
      else:
        ctx.respond("Something went wrong, try again later.")
      
      return False

    message = f"Banned {member.mention}. \nReason: {reason if reason else 'None provided.'}"

    if is_slash:
      ctx.respond(message)
    else:
      ctx.send(message)

  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, member, reason):
    await self.ban_member(ctx, member, reason)
  
  @commands.slash_command(name="ban", description="ban a user")
  @commands.has_permissions(ban_members=True)
  async def slash_ban(self, ctx, member, reason):
    await self.ban_member(ctx, member, reason, is_slash=True)

# FUNCTIONS

def setup(bot):
  bot.add_cog(Ban(bot))