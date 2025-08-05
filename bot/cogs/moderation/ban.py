# bot/cogs/moderation/ban.py

# LIBRARIES AND MODULES


## pycord
import discord
from discord.ext import commands

## pypkg

from bot.constants import *
import bot.console as console

# CLASSES

class Ban(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def ban_member(self,ctx: discord.ApplicationContext, member: discord.Member, reason=None):
    user = ctx.author
    assert ctx.guild
    console.log(f"{user} banned {member} {'for ' + reason if reason else ''}", "LOG")
    try:
        if user==member:
            await ctx.send("Wow you are stupid")
        else:
            await member.ban(reason=reason)
            await ctx.send("Offender BANISHED!")
    except discord.Forbidden:
      console.log(f"Failed to ban {member}, permission denied.", "ERROR")
      await ctx.send("I don't have permission to ban that user.")
    except Exception as e:
      console.log(f"Exception raised: {e}", "ERROR")
      await ctx.send("Something went wrong, try again later.")

    message = f"Banned {member}. \nReason: {reason if reason else 'None provided.'}"



  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx: discord.ApplicationContext, member: discord.Member, reason=None):
    await self.ban_member(ctx, member,reason)

# FUNCTIONS

def setup(bot):
  bot.add_cog(Ban(bot))
