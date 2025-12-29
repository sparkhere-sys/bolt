#!/usr/bin/env python3
# bot/cogs/moderation/timeout.py

# LIBRARIES AND MODULES

## pycord

import discord
from discord.ext import commands

## pypkg

from bot.cogs.moderation.base import Base

# CLASSES

class Timeout(Base):
  def __init__(self, bot):
    super().__init__(bot)
    self.config(timeout=True)
  
  @commands.command()
  @commands.has_permissions(moderate_members=True)
  async def mute(self, ctx: commands.Context, target: discord.Member, duration="30m", *, reason=None):
    await self.action(ctx, target, reason, duration)
  
  @commands.command()
  @commands.has_permissions(moderate_members=True)
  async def unmute(self, ctx: commands.Context, target: discord.Member, *, reason=None):
    self.config(timeout=True, is_un=True)
    await self.action(ctx, target, reason)
  
  @commands.slash_command(name="mute", description="mute a user")
  @commands.has_permissions(moderate_members=True)
  async def slash_mute(self, ctx: discord.ApplicationContext, target: discord.Member, duration: str = "30m", reason: str | None = None):
    await self.action(ctx, target, reason, duration)
  
  @commands.slash_command(name="unmute", description="unmute a previously muted user")
  @commands.has_permissions(moderate_members=True)
  async def slash_unmute(self, ctx: discord.ApplicationContext, target: discord.Member, reason: str | None = None):
    self.config(timeout=True, is_un=True)
    await self.action(ctx, target, reason)

# FUNCTIONS

def setup(bot):
  bot.add_cog(Timeout(bot))