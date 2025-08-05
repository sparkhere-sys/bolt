# bot/cogs/ping.py
# TODO: add docstrings

# LIBRARIES AND MODULES

## pycord

import discord
from discord.ext import commands

## pypkg

import bot.console as console

# CLASSES

class Ping(commands.Cog):
  # TODO: make this DRY

  def __init__(self, bot):
    self.bot = bot
  
  # prefix command

  @commands.command()
  async def ping(self, ctx):
    latency = round(self.bot.latency * 1000)
    user = ctx.author

    console.log(f"Ping requested by {user} ({user.id})", "LOG")
    console.log(f"Latency: {latency}", "LOG")

    await ctx.send(f"Pong! \n{latency}ms")
  
  # slash command
  @commands.slash_command(name="ping", description="ping the bot!")
  async def slash_ping(self, ctx: discord.ApplicationContext):
    latency = round(self.bot.latency * 1000)
    user = ctx.author

    console.log(f"[SLASH] Ping requested by {user} ({user.id})", "LOG")
    console.log(f"Latency: {latency}", "LOG")

    await ctx.respond(f"Pong! \n{latency}ms")

# FUNCTIONS

def setup(bot):
  bot.add_cog(Ping(bot))