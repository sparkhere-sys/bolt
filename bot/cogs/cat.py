#!/usr/bin/python3
# bot/cogs/cat.py

# IMPORTS

from io import BytesIO
import aiohttp

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
    self.session: aiohttp.ClientSession

  async def cog_load(self):
    self.session = aiohttp.ClientSession()

  async def cog_unload(self):
    if self.session:
      await self.session.close()

  async def _cat(self, ctx: ContextType):
    user = ctx.author

    catapi = "https://cataas.com/cat"

    async with self.session.get(catapi) as response:
      response.raise_for_status()
      image = BytesIO(await response.read())
    
    image.seek(0)

    console.log(f"Cat image requested by {user} ({user.id})")

    await utils.say(
      ctx, 
      file=discord.File(image, filename="image.png")
    )

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
