#!/usr/bin/env python3
# bot/cogs/echo.py

# IMPORTS

## pycord

import discord
from discord.ext import commands

## bolt

import bot.console as console
import bot.utils as utils
from bot.constants.types import ContextType

# CLASSES

class Echo(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot

  async def _echo(self, ctx: ContextType, msg: str | None = None) -> None:

    user = ctx.author

    console.log(f"{user} requested an echo.")

    if msg is None:
      console.info("There is nothing to echo, returning.")
      await utils.say(ctx, "There's nothing to echo.", ephemeral=True)
      return

    console.info(f"To be echoed: {msg}")
    await utils.say(ctx, msg)

  # COMMANDS

  # prefix command
  @commands.command()
  async def echo(self, ctx: commands.Context, *, msg=None) -> None: # the * is for msg to be longer than just one word.
    await self._echo(ctx, msg)

  # slash command
  @commands.slash_command(name="echo", description="make the bot say something!")
  @discord.option("message", description="what to say", type=str)
  async def slash_echo(self, ctx: discord.ApplicationContext, msg=None) -> None:
    await self._echo(ctx, msg)

# FUNCTIONS

def setup(bot):

  bot.add_cog(Echo(bot))