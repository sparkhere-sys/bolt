# bot/cogs/ping.py
# TODO: add docstrings

# LIBRARIES AND MODULES

## pycord

import discord
from discord.ext import commands

## pypkg

import bot.console as console
import bot.utils as utils

# CLASSES

class Ping(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  async def _ping(self, ctx, is_slash=False):
    latency = round(self.bot.latency * 1000)
    user = ctx.author

    console.log(f"Ping requested by {user} ({user.id})", "LOG")
    console.log(f"Latency: {latency}ms", "INFO")

    message = f"Pong! \n{latency}ms"
    await utils.say(ctx, message, is_slash=is_slash)

  # prefix command
  @commands.command()
  async def ping(self, ctx: commands.Context):
    await self._ping(ctx)

  # slash command
  @commands.slash_command(name="ping", description="ping the bot!")
  async def slash_ping(self, ctx: discord.ApplicationContext):
    await self._ping(ctx, is_slash=True)

# FUNCTIONS

def setup(bot):
  bot.add_cog(Ping(bot))