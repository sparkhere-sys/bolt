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
    permission="ban_members")

  UNBAN = ActionInfo(
    name="unban",
    verb="unban",
    verb_past="unbanned",
    permission="ban_members")

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

@dataclass
class Case:
  action: Actions
  target: TargetType
  moderator: TargetType # if a moderator leaves the server, we'll only have a discord.User rather than a discord.Member.
  reason: str
  guild: discord.Guild

  active: bool = True
  duration: str | None = None
  case_id: int | None = None # we don't want shadowing, so instead of id, it's case_id
  created_at: datetime | None = field(default_factory=datetime.now)
  expires_at: datetime | None = None # not used for timeouts because we record duration