# bot/utils.py

# LIBRARIES AND MODULES

## pycord

import discord
from discord.ext import commands

# FUNCTIONS

async def say(ctx: discord.ApplicationContext | commands.Context, msg: str, is_slash=False, ephemeral=False):
  if is_slash:
    await ctx.respond(msg, ephemeral=ephemeral)
  else:
    await ctx.send(msg)