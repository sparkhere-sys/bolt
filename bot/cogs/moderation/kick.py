#!/usr/bin/env python3
# bot/cogs/moderation/kick.py

# IMPORTS

## pycord

import discord
from discord.ext import commands

## bolt

from bot.cogs.moderation.base import Base

# CLASSES

class Kick(Base):
  def __init__(self, bot):
    super().__init__(bot)
  
  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx: commands.Context, target: discord.Member, *, reason=None):
    await self._kick(ctx, target, reason)
  
  @commands.slash_command(name="kick", description="kick a member")
  @commands.has_permissions(kick_members=True)
  async def slash_kick(self, ctx: discord.ApplicationContext, target: discord.Member, reason: str | None = None):
    await self._kick(ctx, target, reason)

# FUNCTIONS

def setup(bot):
  bot.add_cog(Kick(bot))