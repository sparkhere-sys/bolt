# bot/cogs/moderation/ban.py

# LIBRARIES AND MODULES

## pycord

import discord
from discord.ext import commands

## pypkg

from bot.constants import *
import bot.console as console
import bot.utils as utils

# CLASSES

class Ban(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def _ban(self, ctx, member, reason=None, is_slash=False):
    user = ctx.author

    if not await utils.assert_guild(ctx, guild=ctx.guild, user=user, is_slash=is_slash):
      return

    try:
      if user == member:
        console.log(f"{user} was an idiot and tried to ban themselves.", "LOG")
        await utils.say(ctx, "You can't ban yourself!", is_slash=is_slash, ephemeral=True)
        return
      
      console.log(f"{user} banned {member}{(' for ' + reason) if reason else '.'}", "LOG")
      await member.ban(reason=reason or 'None provided.')

    except discord.Forbidden:
      console.log(f"Failed to ban {member}, permission denied.", "ERROR")
      await utils.say(ctx, "I don't have permission to ban that user.", is_slash=is_slash, ephemeral=True)

    except Exception as e:
      console.log(f"Exception raised: {e}", "ERROR")
      await utils.say(ctx, "Something went wrong, try again later.", is_slash=is_slash, ephemeral=True)

    message = f"Banned {member.mention}. \nReason: {reason or 'None provided.'}"

    await utils.say(ctx, message, is_slash=is_slash)

  async def _unban(self, ctx, member, reason=None, is_slash=False):
    user = ctx.author

    if not await utils.assert_guild(ctx, guild=ctx.guild, user=user, is_slash=is_slash):
      return

    try:
      if user == member:
        console.log(f"{user} was an idiot and tried to unban themselves.")
        await utils.say(ctx, "You can't unban yourself!", is_slash=is_slash, ephemeral=True)
        return
      
      console.log(f"{user} unbanned {member}{(' for ' + reason) if reason else ''}.", "LOG")
      await ctx.guild.unban(member, reason=reason or 'None provided.')
    
    except discord.Forbidden:
      console.log(f"Failed to unban {member}, permission denied.", "ERROR")
      await utils.say(ctx, "I don't have permission to unban that user.", is_slash=is_slash, ephemeral=True)
      return
    
    except Exception as e:
      console.log(f"Exception raised: {e}", "ERROR")
      await utils.say(ctx, "Something went wrong, try again later.", is_slash=is_slash, ephemeral=True)
      return

    message = f"Unbanned {member.mention}. \nReason: {reason or 'None provided.'}"
    await utils.say(ctx, message, is_slash=is_slash)

  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx: commands.Context, member: discord.Member, *, reason=None):
    await self._ban(ctx, member, reason)
  
  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def unban(self, ctx: commands.Context, member: discord.User, *, reason=None):
    await self._unban(ctx, member, reason)

  @commands.slash_command(name="ban", description="ban a user")
  @commands.has_permissions(ban_members=True)
  async def slash_ban(self, ctx: discord.ApplicationContext, member: discord.Member, reason: str = None):
    await self._ban(ctx, member, reason, is_slash=True)
  
  @commands.slash_command(name="unban", description="ban a user")
  @commands.has_permissions(ban_members=True)
  async def slash_unban(self, ctx: discord.ApplicationContext, member: discord.User, *, reason: str = None):
    await self._unban(ctx, member, reason, is_slash=True)

# FUNCTIONS

def setup(bot):
  bot.add_cog(Ban(bot))
