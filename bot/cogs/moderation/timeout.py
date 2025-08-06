# bot/cogs/moderation/timeout.py

# LIBRARIES AND MODULES

from datetime import timedelta

## pycord

import discord
from discord.ext import commands

## pypkg

import bot.console as console
import bot.utils as utils

# CLASSES

class Timeout(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  def parse_duration(self, duration: str):
    # we are NOT using regex for this
    # regex makes me have an aneurysm

    _duration = duration.lower()

    time_units = {
      "h": 3600, # hours
      "m": 60,   # minutes
      "s": 1     # seconds
    }

    total_seconds = 0
    num = ''

    for char in _duration:
      if char.isdigit():
        num += char
      elif char in time_units:
        if not num:
          return False
        
        total_seconds += int(num) * time_units[char]
        num = ''
      else:
        return False
    
    return total_seconds if total_seconds > 0 else False

  async def _mute(self, ctx, member: discord.member, duration="30m", reason=None, is_slash=False):
    user = ctx.author

    seconds = self.parse_duration(duration)

    if not seconds:
      await utils.say(ctx, "Invalid duration format. Try `1h`, `30m`, `45s`", is_slash=is_slash, ephemeral=True)
      return
    
    try:
      if user == member:
        console.log(f"{user} was an idiot and tried to mute themselves.")
        await utils.say(ctx, "You can't mute yourself!", is_slash=is_slash, ephmeral=True)
        return
      
      await member.timeout_for(timedelta(seconds=seconds), reason=reason or 'None provided.')
      console.log(f"{user} muted {member} for {duration}. Reason: {reason or 'None provided'}", "LOG")

      await utils.say(ctx, f"Muted {member.mention} for {duration}. \nReason: {reason or 'None provided.'}", is_slash=is_slash)

    except discord.Forbidden:
      await utils.say(ctx, "I don't have permission to mute that user.", is_slash=is_slash, ephemeral=True)

    except Exception as e:
      console.log(f"Exception raised: {e}", "ERROR")
      await utils.say(ctx, "Something went wrong, try again later.", is_slash=is_slash, ephemeral=True)
    
  @commands.command()
  @commands.has_permissions(moderate_members=True)
  async def mute(self, ctx: commands.Context, member: discord.member, duration="30m", reason=None):
    await self._mute(ctx, member, duration, reason)
  
  @commands.slash_command(name="mute", description="[moderation] mute a member.")
  @commands.has_permissions(moderate_members=True)
  async def slash_mute(self, ctx: discord.ApplicationContext, member: discord.member, duration="30m", reason=None):
    await self._mute(ctx, member, duration, reason, is_slash=True)

# FUNCTIONS

def setup(bot):
  bot.add_cog(Timeout(bot))