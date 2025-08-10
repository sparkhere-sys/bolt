# bot/utils.py

# LIBRARIES AND MODULES

## pycord

import discord
from discord.ext import commands

## pypkg

import bot.console as console

# FUNCTIONS

async def say(ctx: discord.ApplicationContext | commands.Context, msg: str, is_slash=False, ephemeral=False):
  if is_slash:
    await ctx.respond(msg, ephemeral=ephemeral)
  else:
    await ctx.send(msg)

async def assert_guild(ctx, guild, user, is_slash=False):
  if guild is None:
    console.log(f"{user} tried to run a command where it's not supported.", "LOG")
    await say(ctx, "You can't run that command here!", is_slash=is_slash, ephemeral=True)
    return False
  
  return True
