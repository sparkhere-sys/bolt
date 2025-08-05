import discord
from discord.ext import commands

## pypkg

from bot.constants import *
import bot.console as console

# CLASSES

class Kick(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def Kick_member(self,ctx: discord.ApplicationContext, member: discord.Member, reason=None):
    user = ctx.author
    assert ctx.guild
    console.log(f"{user} Kicked {member} {'for ' + reason if reason else ''}", "LOG")
    try:
        await member.kick(reason=reason)
        await ctx.send("Offender removed.")
    except discord.Forbidden:
      console.log(f"Failed to Kick {member}, permission denied.", "ERROR")
      await ctx.send("I don't have permission to Kick that user.")
    except Exception as e:
      console.log(f"Exception raised: {e}", "ERROR")
      await ctx.send("Something went wrong, try again later.")

    message = f"Banned {member}. \nReason: {reason if reason else 'None provided.'}"


  @commands.has_permissions(ban_members=True)
  @commands.command()
  async def kick(self, ctx: discord.ApplicationContext, member: discord.Member, reason=None):
    await self.Kick_member(ctx, member,reason)

# FUNCTIONS

def setup(bot):
  bot.add_cog(Kick(bot))
