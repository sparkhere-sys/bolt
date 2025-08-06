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
  def __init__(self, bot):
    self.bot = bot
  
  async def send_message(self, ctx, is_slash=False):
    latency = round(self.bot.latency * 1000)
    user = ctx.author

    console.log(f"{'[SLASH] ' if is_slash else ' '}Ping requested by {user} ({user.id})", "LOG")
    console.log(f"Latency: {latency}ms", "INFO")

    message = f"Pong! \n{latency}ms"

    if is_slash:
      await ctx.respond(message)
    else:
      await ctx.send(message)

  # prefix command
  @commands.command()
  async def ping(self, ctx):
    await self.send_message(ctx)
  
  # slash command
  @commands.slash_command(name="ping", description="ping the bot!")
  async def slash_ping(self, ctx: discord.ApplicationContext):
    await self.send_message(ctx, is_slash=True)

# FUNCTIONS

def setup(bot):
  bot.add_cog(Ping(bot))