#!/usr/bin/env python3
# bot/cogs/moderation/base.py

# IMPORTS

from datetime import timedelta # for use with timeout
from typing import Any
from collections.abc import Awaitable # why can't we just put this in typing

## pycord

import discord
from discord.ext import commands

## bolt

import bot.console as console
import bot.utils as utils
from bot.constants.types import ContextType, TargetType
from bot.cogs.moderation.types import Actions, MAX_TIMEOUT_SECONDS, Case
from bot.cogs.moderation.case import CaseModel

# CLASSES

class Base(commands.Cog): # not actually a cog. it just inherits from commands.Cog
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  async def _can_act(self,
                     ctx: ContextType,
                     target: TargetType,
                     action: Actions) -> tuple[bool, str, str]: # i would rather return a dataclass bro
    verb = action.value.verb
    verb_past = action.value.verb_past
    permission = action.value.permission

    if ctx.guild is None:
      await utils.say(ctx, "This command can only be ran in a server.")
      return False, verb, verb_past

    assert isinstance(ctx.author, discord.Member) # pylance stop yelling at me i beg
    user = ctx.author

    if target == user:
      await utils.say(ctx, f"You can't {verb} yourself!", ephemeral=True)
      console.info(f"{user} tried to {verb} themselves.")
      return False, verb, verb_past

    if not self.check_for_permissions(permission, user):
      await utils.say(ctx, f"You don't have permission to {verb} members.", ephemeral=True)
      console.info(f"{user} tried to {verb} {target} but doesn't have permission.")
      return False, verb, verb_past

    return True, verb, verb_past

  def check_for_permissions(self, permission: str, user: discord.Member) -> bool:
    return getattr(user.guild_permissions, permission, False)

  async def _handle_action_call(self,
                                ctx: ContextType,
                                verb: str,
                                target: TargetType,
                                coro: Awaitable[Any]) -> bool:
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
                   target: TargetType,
                   reason: str | None = None,
                   duration: str | None = None) -> None:
    user = ctx.author
    can_act, verb, verb_past = await self._can_act(ctx, target, action)
    if not can_act:
      return

    reason = reason or "None provided."

    console.log(
      f"{user} requested action {action.value.name} ({duration or "no duration"}) on {target} in guild {ctx.guild} with reason {reason}"
    )
    # long ass log bro

    match action:
      case Actions.BAN:
        coro = target.ban(reason=reason) # type: ignore[attr-defined]
        # shut the hell up pylance

      case Actions.UNBAN:
        if ctx.guild is None:
          await utils.say(ctx, "You can't run that command here!")
          return

        coro = ctx.guild.unban(target, reason=reason)
        # NOTE: we're not using type: ignore here
        #       since we're operating on the guild, and not the user.
        #       so this is the only one that works if target is discord.User

      case Actions.KICK:
        coro = target.kick(reason=reason) # type: ignore[attr-defined]

      case Actions.TIMEOUT:
        duration = duration or "30m"

        seconds = utils.parse_duration(duration)
        if not seconds:
          await utils.say(ctx, "Invalid duration format. Try `3d`, `1h`, `30m`, `45s`", ephemeral=True)
          return

        if seconds >= MAX_TIMEOUT_SECONDS:
          await utils.say(ctx, "Dude you can't even mute someone for that long.", ephemeral=True)
          return

        coro = target.timeout_for(timedelta(seconds=seconds), reason=reason) # type: ignore[attr-defined]

      case Actions.UNTIMEOUT:
        coro = target.remove_timeout(reason=reason) # type: ignore[attr-defined]

      case _:
        raise ValueError("Invalid action type")

    if not await self._handle_action_call(ctx, verb, target, coro):
      return

    # say it with me now
    # SHUT UP PYLANCE.
    case = Case(
      action=action,
      target=target,
      moderator=ctx.author,
      reason=reason,
      guild=ctx.guild, # type: ignore[attr-defined]
      duration=duration
    )

    model = CaseModel.from_case(case)
    model.save()

    console.info(f"Saved case #{model.case_id}")

    if action == Actions.TIMEOUT:
      success_message = f"{verb_past.capitalize()} {target.mention} for {duration}. \nReason: {reason}"
    elif action == Actions.UNBAN:
      success_message = f"{verb_past.capitalize()} {getattr(target, 'mention', str(target))}. \nReason: {reason}"
    else:
      success_message = f"{verb_past.capitalize()} {target.mention}. \nReason: {reason}"

    await utils.say(ctx, success_message)

  # HELPERS

  async def _ban(self, ctx: ContextType, target: discord.Member, reason: str | None = None) -> None:
    await self.action(ctx, Actions.BAN, target, reason)

  async def _unban(self, ctx: ContextType, target: discord.User, reason: str | None = None) -> None:
    await self.action(ctx, Actions.UNBAN, target, reason)

  async def _kick(self, ctx: ContextType, target: discord.Member, reason: str | None = None) -> None:
    await self.action(ctx, Actions.KICK, target, reason)

  async def _mute(self, ctx: ContextType, target: discord.Member, duration: str = "30m", reason: str | None = None) -> None:
    await self.action(ctx, Actions.TIMEOUT, target, reason, duration=duration)

  async def _unmute(self, ctx: ContextType, target: discord.Member, reason: str | None = None) -> None:
    await self.action(ctx, Actions.UNTIMEOUT, target, reason)