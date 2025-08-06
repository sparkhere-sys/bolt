# bot/cogs/moderation/kick.py

# LIBRARIES AND MODULES

## pycord

import discord
from discord.ext import commands

## pypkg

from bot.constants import *
import bot.console as console

# CLASSES

class Kick(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def kick_member(self, ctx, member: discord.Member, reason=None, is_slash=False):
    user = ctx.author

    assert ctx.guild

    try:
      if user == member:
        console.log(f"{user} was an idiot and tried to kick themselves.", "LOG")
        if is_slash:
          await ctx.send("You can't kick yourself! \nThere's a 'leave server' button, you know.")
        else:
          await ctx.respond("You can't kick yourself! \nThere's a 'leave server' button, you know.")
      else:
        console.log(f"{user} Kicked {member} {'for ' + reason if reason else ''}", "LOG")
        if reason is None:
          await member.kick(reason="None provided.")
        else:
          await member.kick(reason=reason)

    except discord.Forbidden:
      console.log(f"Failed to kick {member}, permission denied.", "ERROR")
      await ctx.send("I don't have permission to kick that user.")

    except Exception as e:
      console.log(f"Exception raised: {e}", "ERROR")
      await ctx.send("Something went wrong, try again later.")

    message = f"Kicked {member}. \nReason: {reason if reason else 'None provided.'}"

    if is_slash:
       await ctx.respond(message)
    else:
       await ctx.send(message)

  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx: discord.ApplicationContext, member: discord.Member, reason=None):
    await self.kick_member(ctx, member, reason)
  
  @commands.slash_command(name="kick", description="kick a member.")
  @commands.has_permissions(kick_members=True)
  async def slash_kick(self, ctx: discord.ApplicationContext, member: discord.Member, reason=None):
     await self.kick_member(ctx, member, reason)

# FUNCTIONS

def setup(bot):
  bot.add_cog(Kick(bot))
