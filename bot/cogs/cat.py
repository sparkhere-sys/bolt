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
    # IMPORTANT
    # i have genuinely checked pycord's source code,
    # this function literally NEVER runs
    # but for some reason, cog_unload() DOES.
    # i have no idea why.
    # if i were that dedicated i could open a PR in pycord's repo.
    # -spark
    
    console.debug("Creating session")
    self.session = aiohttp.ClientSession()

  async def cog_unload(self):
    if self.session:
      await self.session.close()

  async def _cat(self, ctx: ContextType):
    if not hasattr(self, "session"): # sometimes cog_load() just NEVER runs for some unknown reason
      self.session = aiohttp.ClientSession()

    user = ctx.author

    console.log(f"Cat image requested by {user} ({user.id})")

    catapi = "https://cataas.com/cat"

    timeout = aiohttp.ClientTimeout(30)

    try:
      async with self.session.get(catapi, timeout=timeout) as response:
        response.raise_for_status()
        image = BytesIO(await response.read())
    except aiohttp.ServerTimeoutError:
      console.error_traceback()
      await utils.say(ctx, "Your request timed out.", ephemeral=True)
      return
    except aiohttp.ClientError:
      console.error_traceback()
      await utils.say(ctx, "Something went wrong. Try again later.", ephemeral=True)
      return
    except Exception:
      console.error_traceback()
      await utils.say(ctx, "Something went wrong. Try again later.", ephemeral=True)
      return

    image.seek(0)

    console.info("Cat sent.")

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
