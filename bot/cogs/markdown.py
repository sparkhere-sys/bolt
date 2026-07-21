#!/usr/bin/env python3
# bot/cogs/markdown.py
'''
Paired with the md files in bot/markdown and bot/markdown/markdown.py.

Replaces help.py and invite.py from before.

Contains the MarkdownCommands cog.
'''
# you have no idea how many times i wrote "markdown" while i was writing this. -spark

# LIBRARIES AND MODULES

import discord
from discord.ext import commands

# pypkg

import bot.console as console
import bot.utils as utils
import bot.markdown.markdown as markdown
import functools

# CLASSES

class MarkdownCommands(commands.Cog):
  '''
  Handles the markdown-based commands like `help` and `invite`.
  '''

  def __init__(self, bot):
    self.bot = bot
  
  @functools.cache
  def fetch_markdown_file(self, cmd_type: str) -> str: # cmd_type is a string because i dont know how to use enums.
    '''
    This function fetches the markdown file for the given command type, 
    finds and replaces constants, 
    then returns the final string.

    ### Parameters
    cmd_type (str): the type of command to fetch the markdown file for.

    ### Returns
    str: the final markdown string with constants replaced.
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
    This function is a bot command.

    Sends the help message in the channel the command was invoked in.
    '''

    user = ctx.author
    console.log(f"Help requested by {user} ({user.id})")

    message = self.fetch_markdown_file("help")
    await utils.say(ctx, message)
  
  async def _invite(self, ctx):
    '''
    This function is a bot command.

    Sends the invite link message in the channel the command was invoked in.
    '''

    user = ctx.author
    console.log(f"Invite requested by {user} ({user.id})")

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
  Adds the MarkdownCommands cog to the bot
  '''

  bot.add_cog(MarkdownCommands(bot))
