#!/usr/bin/env python3
# bot/cogs/ping.py
'''
Contains the Ping cog.
'''

# LIBRARIES AND MODULES

import time

## pycord

import discord
from discord.ext import commands

## pypkg

import bot.console as console
import bot.utils as utils

# CLASSES

class Ping(commands.Cog):
  '''
  Handles the ping and uptime commands.
  '''

  def __init__(self, bot):
    self.bot = bot
  
  async def _ping(self, ctx: discord.ApplicationContext | commands.Context):
    '''
    This function is a bot command.

    Pings the bot and says the latency in ms in the channel the command was run in.

    ### Parameters
    * ctx: discord.ApplicationContext | commands.Context: The context of the command.

    ### Returns
    nothing.

    ### Raises
    nothing.
    '''

    user = ctx.author

    latency = round(self.bot.latency * 1000)

    console.log(f"Ping requested by {user} ({user.id})")
    console.log(f"Latency: {latency}ms")

    await utils.say(ctx, f"Pong! \n{latency}ms")
  
  async def _uptime(self, ctx: discord.ApplicationContext | commands.Context):
    '''
    This function is a bot command.

    Gets the bot's start_time attribute and calculates the uptime,
    then sends it in the channel the command was invoked in.

    ### Parameters
    * ctx: discord.ApplicationContext | commands.Context: The context of the command.

    ### Returns
    nothing.

    ### Raises
    nothing.
    '''

    user = ctx.author

    console.log(f"Uptime requested by {user} ({user.id})")
    
    delta = int(time.time() - self.bot.start_time)

    days, remainder = divmod(delta, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    console.log(f"Uptime: {days}d {hours}h {minutes}m {seconds}s")
    await utils.say(ctx, f"Uptime: {days}d {hours}h {minutes}m {seconds}s")

  # COMMANDS

  @commands.command()
  async def ping(self, ctx: commands.Context):
    await self._ping(ctx)

  @commands.slash_command(name="ping", description="ping the bot!")
  async def slash_ping(self, ctx: discord.ApplicationContext):
    await self._ping(ctx)
  
  @commands.command()
  async def uptime(self, ctx: commands.Context):
    await self._uptime(ctx)
  
  @commands.slash_command(name="uptime", description="see how long the bot has been running for!")
  async def slash_uptime(self, ctx: discord.ApplicationContext):
    await self._uptime(ctx)

# FUNCTIONS

def setup(bot):
  '''
  Adds the Ping cog to the bot
  '''

  bot.add_cog(Ping(bot))