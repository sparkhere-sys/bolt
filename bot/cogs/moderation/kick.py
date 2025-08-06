import discord
from discord.ext import commands

## pypkg

from bot.constants import *
import bot.console as console

# CLASSES

class Kick(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def kick_member(self, ctx: discord.ApplicationContext, member: discord.Member, reason=None, is_slash=False):
    user = ctx.author

    assert ctx.guild
    console.log(f"{user} Kicked {member} {'for ' + reason if reason else ''}", "LOG")

    try:
        if user == member:
            if is_slash:
              await ctx.send("You can't kick yourself! \nThere's a 'leave server' button, you know.")
            else:
               await ctx.respond("You can't kick yourself! \nThere's a 'leave server' button, you know.")
        else:
            await member.kick(reason=reason)
    except discord.Forbidden:
      console.log(f"Failed to kick {member}, permission denied.", "ERROR")
      await ctx.send("I don't have permission to Kick that user.")
    except Exception as e:
      console.log(f"Exception raised: {e}", "ERROR")
      await ctx.send("Something went wrong, try again later.")

    message = f"Kicked {member}. \nReason: {reason if reason else 'None provided.'}"
    if is_slash:
       ctx.respond(message)
    else:
       ctx.send(message)

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
