#!/usr/bin/env python3
# bot/cogs/moderation/base.py
'''
Contains the base class for moderation actions.
'''
# this one was desperate for docstrings before the others lol

# LIBRARIES AND MODULES

from datetime import timedelta # for use with timeout

## pycord

import discord
from discord.ext import commands

## pypkg

from bot.constants.moderation import *
import bot.console as console
import bot.utils as utils

# CLASSES

class Base(commands.Cog): # not actually a cog. it just inherits from commands.Cog
  '''
  Base class for moderation actions.

  ### Usage
  * Create a new class that extends this one.
  * Treat that new class as a regular cog.
  * In the __init__() method of that class, call super().__init__(bot),
    and then call self.config() with the appropriate configuration kwargs.
  * Then create your commands as normal, and inside them call self.action() with the correct arguments.
  '''

  def __init__(self, bot):
    self.bot = bot

  def config(self, **kwargs):
    '''
    This function configures the cog for a specific moderation action.
    ### Accepted boolean kwargs:
    * timeout
    * ban
    * kick
    * is_un

    ### Returns
    nothing.

    ### Raises
    nothing.
    '''
  
    self.timeout = kwargs.get("timeout", False)
    self.ban = kwargs.get("ban", False)
    self.kick = kwargs.get("kick", False)
    self.is_un = kwargs.get("is_un", False) # genuinely one of the dumbest names for a variable ever but it works (i hope)

    self.use_duration = self.timeout and not self.is_un # temporary bans haven't been added yet and will be pretty hard to add

    dict_map = {
      "ban": (("ban", "banned"), ("unban", "unbanned")),
      "kick": (("kick", "kicked"), ("kick", "kicked")),
      "timeout": (("mute", "muted"), ("unmute", "unmuted")),
    }

    if self.ban:
      mapping_key = "ban"
    elif self.kick:
      mapping_key = "kick"
    elif self.timeout:
      mapping_key = "timeout"

    self.verb, self.verb_past = dict_map[mapping_key][0 if not self.is_un else 1]
  
  def check_for_permissions(self, perm: str, user, perm_map: dict) -> bool:
    '''
    This command checks if the user has the required permissions to perform the action.

    ### Parameters
    * perm (str): the permission to check for (e.g. "ban", "kick", "timeout")
    * user (discord.Member): the user to check the permissions for
    * perm_map (dict): the permission mapping to use (e.g. perm_map or un_perm_map)

    ### Returns
    * bool: True if the user has the required permissions, False otherwise

    ### Raises
    nothing.
    '''

    if not perm:
      return False # early return
    
    if not perm in perm_map:
      return False # ditto
    
    if getattr(user.guild_permissions, perm_map[perm], False):
      return True # ditto
    
    return False

  async def action(self,
                   ctx: commands.Context | discord.ApplicationContext, 
                   target,
                   reason: str | None = None, 
                   duration: str = "30m"):
    '''
    This function performs the action specified by the configuration.

    ### Parameters
    * ctx (discord.ApplicationContext | commands.Context): the context of the command.
    * target (discord.Member | discord.User): the member to perform the action on.
    * reason (str | None): the reason for the action. default: None
    * duration (str): the duration of the action (only for timeout). default: "30m"

    ### Returns
    nothing.

    ### Raises
    * ValueError: if an invalid action_type is specified.
    '''

    user = ctx.author
    reason = reason or "None provided."
    
    # get action type
    if self.ban:
      action_type = "ban" if not self.is_un else "unban"
    elif self.kick:
      action_type = "kick"
    elif self.timeout:
      action_type = "timeout" if not self.is_un else "untimeout"

    ## checks

    if ctx.guild is None:
      await utils.say(ctx, "This command can only be ran in a server.")
      return
    
    if target == user:
      await utils.say(ctx, f"You can't {self.verb} yourself!", ephemeral=True)
      console.info(f"{user} tried to {self.verb} themselves.")
      return
    
    if not self.check_for_permissions(action_type, user, perm_map=perm_map if not self.is_un else un_perm_map):
      await utils.say(ctx, f"You don't have permission to {self.verb} members.", ephemeral=True)
      console.info(f"{user} tried to {self.verb} {target} but doesn't have permission.")
      return

    # that's a lot of console.log() calls
    console.log(f"An action has been requested.")
    console.info(f"Action type: {action_type}")
    console.info(f"Target: {target} ({target.id})")
    console.info(f"Requested by: {user} ({user.id})")
    console.info(f"Reason: {reason}")
    console.info(f"Duration: {duration}")
    console.info(f"In guild: {ctx.guild} ({ctx.guild.id})")
    
    ## duration parsing
    
    if self.use_duration:
      seconds = utils.parse_duration(duration)
      
      if not seconds:
        await utils.say(ctx, "Invalid duration format. Try `3d`, `1h`, `30m`, `45s`", ephemeral=True)
        return
      
      # if seconds < 0 check is not required. 
      # parse_duration() will just kill itself if it sees a negative number anyway

      if seconds >= 2419200: # as in, 28 days.
        if self.ban:
          seconds = 0 # anything larger than 28 days and discord will die so we just make it a perma ban
        elif self.timeout: # made this into an elif just to sanity check
          await utils.say(ctx, "Dude you can't even mute someone for that long.", ephemeral=True)
          return
      
    ## action execution

    try:
      match action_type:
        # not is_un
        case "ban":
          await target.ban(reason=reason)
        
        case "timeout":
          await target.timeout_for(timedelta(seconds=seconds), reason=reason)
        
        case "kick":
          await target.kick(reason=reason)
        
        # is_un
        case "unban":
          await ctx.guild.unban(target, reason=reason)

        case "untimeout":
          await target.remove_timeout(reason=reason)

        # literally anything else
        # NOTE: this case should never be reached if the code is working properly.
        #       remove?
        case _:
          raise ValueError("that action_type doesn't exist dude.")
    
    except discord.Forbidden:
      console.error(f"Failed to {self.verb} {target}, permission denied.")
      await utils.say(ctx, f"I don't have permission to {self.verb} that user.", ephemeral=True)
      return
    
    except discord.HTTPException:
      console.error(f"Failed to {self.verb} {target}, HTTPException raised.")
      await utils.say(ctx, f"Something went wrong while trying to {self.verb} that user.", ephemeral=True)
      return
    
    except Exception as e:
      console.error(f"Exception raised: {e}")
      await utils.say(ctx, "Something went wrong. Try again later.", ephemeral=True)
      return
    
    console.info(f"{user} {self.verb_past} {target}{(' for ' + duration) if self.use_duration else ''} for: {reason}")

    success_message = f"{self.verb_past.capitalize()} {target.mention}{(' for ' + duration) if self.use_duration else ''}. \nReason: {reason}"
    await utils.say(ctx, success_message)