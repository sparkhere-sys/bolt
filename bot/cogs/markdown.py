#!/usr/bin/env python3
# bot/cogs/markdown.py
'''
paired with the md files in bot/markdown and bot/markdown/markdown.py.
replaces help.py and invite.py from before.

you have no idea how many times i've typed "markdown" while writing this.
'''

# LIBRARIES AND MODULES

import discord
from discord.ext import commands

# pypkg

import bot.console as console
import bot.utils as utils
import bot.markdown.markdown as markdown

# CLASSES

class MarkdownCommands(commands.Cog):
  '''
  handles the markdown-based commands like help and invite.
  '''

  def __init__(self, bot):
    self.bot = bot
  
  def fetch_markdown_file(self, cmd_type: str): # cmd_type is a string because i dont know how to use enums.
    '''
    <method>

    fetches the markdown file for the given command type, finds and replaces constants, then returns the final string.
    '''

    # TODO: refactor to use enums for cmd_type
    match cmd_type:
      case "help":
        md_class = markdown.Help()
      case "invite":
        md_class = markdown.Invite()
      case _:
        raise ValueError("that cmd_type doesn't exist dude.")
      
    with open(md_class.path, "r", encoding="utf-8") as f:
      md_data = f.read()
    
    for find, replace in md_class.find_and_replace.items():
      md_data = md_data.replace(find, replace)
    
    return md_data

  async def _help(self, ctx):
    '''
    <_command>

    sends a help message in the channel the command was invoked in
    '''

    user = ctx.author
    console.log(f"Help requested by {user} ({user.id})", "LOG")

    message = self.fetch_markdown_file("help")
    await utils.say(ctx, message)
  
  async def _invite(self, ctx):
    '''
    <_command>

    sends an invite link message in the channel the command was invoked in
    '''

    user = ctx.author
    console.log(f"Invite requested by {user} ({user.id})", "LOG")

    message = self.fetch_markdown_file("invite")
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
  '''
  adds MarkdownCommands cog to the bot
  '''

  bot.add_cog(MarkdownCommands(bot))