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
  
  async def ban_member(self, ctx, member: discord.Member, reason=None, is_slash=False):
    user = ctx.author

    assert ctx.guild

    try:
      if user == member:
        console.log(f"{user} was an idiot and tried to ban themselves.", "LOG")

        if is_slash:
          await ctx.respond("You can't ban yourself! \nThere's a 'leave server' button, you know.")
        else:
          await ctx.send("You can't ban yourself! \nThere's a 'leave server' button, you know.")
        
        return
      else:
        console.log(f"{user} banned {member} {'for ' + reason or ''}", "LOG")
        if reason is None:
          await member.ban(reason="None provided.")
        else:
          await member.ban(reason=reason)

    except discord.Forbidden:
      console.log(f"Failed to ban {member}, permission denied.", "ERROR")
      if is_slash:
        await ctx.respond("I don't have permission to ban that user.")
      else:
        await ctx.send("I don't have permission to ban that user.")

    except Exception as e:
      console.log(f"Exception raised: {e}", "ERROR")
      if is_slash:
        await ctx.respond("Something went wrong, try again later.")
      else:
        await ctx.send("Something went wrong, try again later.")

    message = f"Banned {member.mention}. \nReason: {reason or 'None provided.'}"

    if is_slash:
      await ctx.respond(message)
    else:
      await ctx.send(message)

  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx: commands.Context, member: discord.Member, reason=None):
    await self.ban_member(ctx, member, reason)
  
  @commands.slash_command(name="ban", description="ban a user")
  @commands.has_permissions(ban_members=True)
  async def slash_ban(self, ctx: discord.ApplicationContext, member: discord.Member, reason=None):
    await self.ban_member(ctx, member,reason)

# FUNCTIONS

def setup(bot):
  bot.add_cog(Ban(bot))
