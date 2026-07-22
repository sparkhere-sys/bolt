#!/usr/bin/env python3

# IMPORTS

from enum import Enum
from dataclasses import dataclass

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