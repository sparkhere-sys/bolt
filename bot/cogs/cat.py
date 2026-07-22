#!/usr/bin/python3
# bot/cogs/cat.py

# IMPORTS

from io import BytesIO
import requests

## pycord

from discord.ext import commands
import discord

# bolt

import bot.utils as utils
import bot.console as console
from bot.constants.types import ContextType

# CLASSES

class Cat(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  async def _cat(self, ctx: ContextType):
    user = ctx.author

    catapi = "https://cataas.com/cat"
    response = requests.get(catapi) # NOTE: since http is synchronous, this bites us in the back. move to aiohttp is a TODO
    image = BytesIO(response.content)
    image.seek(0)

    console.log(f"Cat image requested by {user} ({user.id})")

    await utils.say(ctx, file=discord.File(image, filename="image.png")) # type: ignore

  # COMMANDS

  @commands.command()
  async def cat(self, ctx):
    await self._cat(ctx)

  @commands.slash_command(name="cat", description="sends a random cat image")
  async def slash_cat(self, ctx):
    await self._cat(ctx)

# FUNCTIONS

def setup(bot):

  bot.add_cog(Cat(bot))
