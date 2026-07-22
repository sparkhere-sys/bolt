#!/usr/bin/env python3
# bot/cogs/moderation/base.py

# IMPORTS

from datetime import timedelta # for use with timeout
from enum import Enum
from typing import Union

## pycord

import discord
from discord.ext import commands

## bolt

from bot.constants.moderation import *
import bot.console as console
import bot.utils as utils

# CONSTANTS AND VARIABLES

MAX_TIMEOUT_SECONDS = 28 * 24 * 60 * 60  # 28 days

ContextType = Union[commands.Context, discord.ApplicationContext]

# ENUMS

class Actions(Enum):
  BAN = "ban"
  UNBAN = "unban"
  KICK = "kick"
  TIMEOUT = "timeout"
  UNTIMEOUT = "untimeout"

# CLASSES

class Base(commands.Cog): # not actually a cog. it just inherits from commands.Cog
  def __init__(self, bot):
    self.bot = bot

  async def _can_act(self, ctx, target, action_name: str, allow_user_target: bool = False):
    user = ctx.author

    mapping = {
      "ban": {"verb": "ban", "verb_past": "banned", "uses_duration": False},
      "unban": {"verb": "unban", "verb_past": "unbanned", "uses_duration": False},
      "kick": {"verb": "kick", "verb_past": "kicked", "uses_duration": False},
      "timeout": {"verb": "mute", "verb_past": "muted", "uses_duration": True},
      "untimeout": {"verb": "unmute", "verb_past": "unmuted", "uses_duration": False},
    }

    if action_name not in mapping:
      return False, False, "action", "acted"

    info = mapping[action_name]
    verb = info["verb"]
    verb_past = info["verb_past"]
    uses_duration = info["uses_duration"]

    if ctx.guild is None:
      await utils.say(ctx, "This command can only be ran in a server.")
      return False, uses_duration, verb, verb_past

    try:
      if not allow_user_target and target == user:
        await utils.say(ctx, f"You can't {verb} yourself!", ephemeral=True)
        console.info(f"{user} tried to {verb} themselves.")
        return False, uses_duration, verb, verb_past
    except Exception:
      pass

    perm_map_used = un_perm_map if action_name in ("unban", "untimeout") else perm_map

    if not self.check_for_permissions(action_name, user, perm_map=perm_map_used):
      await utils.say(ctx, f"You don't have permission to {verb} members.", ephemeral=True)
      console.info(f"{user} tried to {verb} {target} but doesn't have permission.")
      return False, uses_duration, verb, verb_past

    return True, uses_duration, verb, verb_past
  
  def check_for_permissions(self, perm: str, user, perm_map: dict) -> bool:
    if not perm:
      return False # early return
    
    if not perm in perm_map:
      return False # ditto
    
    if getattr(user.guild_permissions, perm_map[perm], False):
      return True # ditto
    
    return False

  async def _handle_action_call(self, ctx: ContextType, verb: str, target, coro) -> bool:
    try:
      await coro

    except discord.Forbidden:
      console.error(f"Failed to {verb} {target}, permission denied.")
      await utils.say(ctx, f"I don't have permission to {verb} that user.", ephemeral=True)
      return False
    
    except discord.HTTPException:
      console.error(f"Failed to {verb} {target}, HTTPException raised.")
      await utils.say(ctx, f"Something went wrong while trying to {verb} that user.", ephemeral=True)
      return False
    
    except Exception as e:
      console.error(f"Exception raised: {e}")
      await utils.say(ctx, "Something went wrong. Try again later.", ephemeral=True)
      return False

    return True

  async def action(self, 
                   ctx: ContextType, 
                   action: Actions, 
                   target, 
                   reason: str | None = None, 
                   duration: str | None = None):
    user = ctx.author
    action_name = action.value
    ok, _uses_duration, verb, verb_past = await self._can_act(ctx, target, action_name, allow_user_target=action_name in ("unban",))
    if not ok:
      return

    reason = reason or "None provided."

    console.log(f"{user} requested action {action_name} on {target} in guild {ctx.guild}.")

    match action:
      case Actions.BAN:
        coro = target.ban(reason=reason)

      case Actions.UNBAN:
        if ctx.guild is None:
          await utils.say(ctx, "You can't run that command here!")
          return
        coro = ctx.guild.unban(target, reason=reason)

      case Actions.KICK:
        coro = target.kick(reason=reason)

      case Actions.TIMEOUT:
        duration = duration or "30m"

        seconds = utils.parse_duration(duration)
        if not seconds:
          await utils.say(ctx, "Invalid duration format. Try `3d`, `1h`, `30m`, `45s`", ephemeral=True)
          return

        if seconds >= MAX_TIMEOUT_SECONDS:
          await utils.say(ctx, "Dude you can't even mute someone for that long.", ephemeral=True)
          return

        coro = target.timeout_for(timedelta(seconds=seconds), reason=reason)

      case Actions.UNTIMEOUT:
        coro = target.remove_timeout(reason=reason)

      case _:
        raise ValueError("Invalid action type")

    if not await self._handle_action_call(ctx, verb, target, coro):
      return

    ## console.info(f"{ctx.author} {verb_past} {target} for: {reason}")

    if action == Actions.TIMEOUT:
      success_message = f"{verb_past.capitalize()} {target.mention} for {duration}. \nReason: {reason}"
    elif action == Actions.UNBAN:
      success_message = f"{verb_past.capitalize()} {getattr(target, 'mention', str(target))}. \nReason: {reason}"
    else:
      success_message = f"{verb_past.capitalize()} {target.mention}. \nReason: {reason}"
    
    await utils.say(ctx, success_message)

  # HELPERS

  async def _ban(self, ctx: ContextType, target: discord.Member, reason: str | None = None):
    await self.action(ctx, Actions.BAN, target, reason)

  async def _unban(self, ctx: ContextType, target: discord.User, reason: str | None = None):
    await self.action(ctx, Actions.UNBAN, target, reason)

  async def _kick(self, ctx: ContextType, target: discord.Member, reason: str | None = None):
    await self.action(ctx, Actions.KICK, target, reason)

  async def _mute(self, ctx: ContextType, target: discord.Member, duration: str = "30m", reason: str | None = None):
    await self.action(ctx, Actions.TIMEOUT, target, reason, duration=duration)

  async def _unmute(self, ctx: ContextType, target: discord.Member, reason: str | None = None):
    await self.action(ctx, Actions.UNTIMEOUT, target, reason)