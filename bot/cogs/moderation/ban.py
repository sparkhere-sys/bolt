#!/usr/bin/env python3
# bot/cogs/moderation/ban.py
'''
Contains the Ban cog.
'''

# LIBRARIES AND MODULES

## pycord

import discord
from discord.ext import commands

## pypkg

from bot.cogs.moderation.base import Base

# CLASSES

class Ban(Base):
  '''
  Inherits from Base and handles the ban and unban commands.
  '''

  def __init__(self, bot):
    super().__init__(bot)
  
  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx: commands.Context, target: discord.Member, *, reason=None):
    self.config(ban=True, is_un=False)
    await self.action(ctx, target, reason)
  
  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def unban(self, ctx: commands.Context, target: discord.User, *, reason=None):
    self.config(ban=True, is_un=True)
    await self.action(ctx, target, reason)
  
  @commands.slash_command(name="ban", description="ban a user")
  @commands.has_permissions(ban_members=True)
  async def slash_ban(self, ctx: discord.ApplicationContext, target: discord.Member, reason: str | None = None):
    self.config(ban=True, is_un=False)
    await self.action(ctx, target, reason)

  @commands.slash_command(name="unban", description="unban a previously banned user")
  @commands.has_permissions(ban_members=True)
  async def slash_unban(self, ctx: discord.ApplicationContext, target: discord.User, reason: str | None = None):
    self.config(ban=True, is_un=True)
    await self.action(ctx, target, reason)

# FUNCTIONS

def setup(bot):
  '''
  Adds the Ban cog to the bot.
  '''
  
  bot.add_cog(Ban(bot))