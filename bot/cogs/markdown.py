#!/usr/bin/env python3
# bot/cogs/markdown.py
# you have no idea how many times i wrote "markdown" while i was writing this. -spark

# IMPORTS

from enum import Enum
import functools

## pycord

import discord
from discord.ext import commands

## bolt

import bot.console as console
import bot.utils as utils
import bot.markdown.markdown as markdown
from bot.constants.types import ContextType

# ENUMS AND DATACLASSES

class MarkdownFiles(Enum):
  HELP   = markdown.Help()
  INVITE = markdown.Invite()

# CLASSES

class MarkdownCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @functools.cache
  def fetch_markdown_file(self, cmd_type: MarkdownFiles) -> str:
    md_class = cmd_type.value      
    with open(md_class.path, "r", encoding="utf-8") as f:
      md_data = f.read()
    
    for find, replace in md_class.find_and_replace.items():
      md_data = md_data.replace(find, replace)
    
    return md_data

  async def _help(self, ctx: ContextType) -> None:
    user = ctx.author
    console.log(f"Help requested by {user} ({user.id})")

    message = self.fetch_markdown_file(MarkdownFiles.HELP)
    await utils.say(ctx, message)
  
  async def _invite(self, ctx: ContextType) -> None:
    user = ctx.author
    console.log(f"Invite requested by {user} ({user.id})")

    message = self.fetch_markdown_file(MarkdownFiles.INVITE)
    await utils.say(ctx, message)
  
  # COMMANDS
  ## help

  @commands.command()
  async def help(self, ctx: commands.Context):
    await self._help(ctx)
  
  @commands.slash_command(name="help", description="show the help message.")
  async def slash_help(self, ctx: discord.ApplicationContext):
    await self._help(ctx)
  
  ## invite

  @commands.command()
  async def invite(self, ctx: commands.Context):
    await self._invite(ctx)
  
  @commands.slash_command(name="invite", description="invite the bot to your server!")
  async def slash_invite(self, ctx: discord.ApplicationContext):
    await self._invite(ctx)

# FUNCTIONS

def setup(bot):
  bot.add_cog(MarkdownCommands(bot))
