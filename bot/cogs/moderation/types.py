#!/usr/bin/env python3

# IMPORTS

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime

## pycord

import discord

## bolt

from bot.constants.types import TargetType

# CONSTANTS AND VARIABLES

MAX_TIMEOUT_SECONDS = 28 * 24 * 60 * 60  # 28 days

# ENUMS AND DATACLASSES

@dataclass(frozen=True)
class ActionInfo:
  name: str
  verb: str
  verb_past: str
  permission: str

class Actions(Enum):
  BAN = ActionInfo(
    name="ban",
    verb="ban",
    verb_past="banned",
    permission="ban_members"
  )

  UNBAN = ActionInfo(
    name="unban",
    verb="unban",
    verb_past="unbanned",
    permission="ban_members"
  )

  KICK = ActionInfo(
    name="kick",
    verb="kick",
    verb_past="kicked",
    permission="kick_members"
  )

  TIMEOUT = ActionInfo(
    name="timeout",
    verb="mute",
    verb_past="muted",
    permission="moderate_members"
  )

  UNTIMEOUT = ActionInfo(
    name="untimeout",
    verb="unmute",
    verb_past="unmuted",
    permission="moderate_members"
  )

  WARN = ActionInfo(
    name="warn",
    verb="warn",
    verb_past="warned",
    permission="moderate_members"
  )

@dataclass
class Case:
  action: Actions
  target: TargetType
  moderator: TargetType # if a moderator leaves the server, we'll only have a discord.User 
                        # rather than a discord.Member.
  reason: str
  guild: discord.Guild

  active: bool = True
  duration: str | None = None
  case_id: int | None = None # we don't want shadowing
  created_at: datetime | None = field(default_factory=datetime.now)
  expires_at: datetime | None = None # not used for timeouts because we record duration
                                     # and discord automatically untimeouts after
                                     # the duration ends, unlike with bans which are
                                     # permanent only on the discord side.
  
  # NOTE: there is *some* confusion regarding timeout cases being active even after their duration
  #       has ended. for all intents and purposes, this is fully intentional, but for the sake of
  #       user-friendliness, we may or may not schedule closing timeout cases.