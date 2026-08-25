#!/usr/bin/env python3
# bot/cogs/moderation/case_commands.py

# IMPORTS

## pycord

import discord
from discord.ext import commands

## bolt

from bot.cogs.moderation.types import Actions
from bot.constants.types import ContextType, TargetType
from bot.constants.toml import prefix
import bot.cogs.moderation.case as case
import bot.utils as utils
import bot.console as console

# CLASSES

class CaseCommands(commands.Cog):
  case_group = discord.SlashCommandGroup("case", "View and manage cases.")

  def __init__(self, bot):
    self.bot = bot

  def _has_moderation_perm(self, ctx: ContextType) -> bool:
    if not isinstance(ctx.author, discord.Member):
      return False

    permissions = ctx.author.guild_permissions

    return any((
      permissions.moderate_members,
      permissions.kick_members,
      permissions.ban_members,
    ))

  def _has_case_perm(self, ctx: ContextType, model: case.CaseModel) -> bool:
    if not isinstance(ctx.author, discord.Member):
      return False

    action = Actions[model.action.upper()] # thank you python for letting us do this
    permission = action.value.permission

    return getattr(ctx.author.guild_permissions, permission)

  async def _case(self, ctx: ContextType, case_id: int | None = None) -> None:
    if case_id is None:
      await utils.say(ctx, "You need to provide a case ID.")
      return

    if ctx.guild is None:
      await utils.say(ctx, "You can't run that command here!")
      return

    database = case.get_database(ctx.guild.id)
    model = case.get_case(database, case_id)

    if model is None:
      await utils.say(ctx, "That case doesn't exist.")
      return

    if not self._has_moderation_perm(ctx):
      await utils.say(ctx, "You don't have permission.")
      return

    message = ( # implicit string concatenation from python
      f"Case #{model.case_id}\n"
      f"Action: {model.action.capitalize()}\n"
      f"Target: <@{model.target}>\n"
      f"Moderator: <@{model.moderator}>\n"
      f"Reason: {model.reason}\n"
      f"Duration: {model.duration or 'none'}\n"
      f"Active: {'yes' if model.active else 'no'}"
    )

    await utils.say(ctx, message)

  async def _revoke(self, ctx: ContextType, case_id: int | None = None) -> None:
    if case_id is None:
      await utils.say(ctx, "You need to provide a case ID.")
      return

    if ctx.guild is None:
      await utils.say(ctx, "You can't run that command here!")
      return

    database = case.get_database(ctx.guild.id)
    model = case.get_case(database, case_id)

    if model is None:
      await utils.say(ctx, "That case doesn't exist.")
      return

    if not self._has_case_perm(ctx, model):
      await utils.say(ctx, "You don't have permission.")
      return

    result = case.revoke_case(database, case_id)

    if result is None:
      await utils.say(ctx, "That case doesn't exist.")
      return

    if not result:
      await utils.say(ctx, "That case is already inactive.")
      return

    await utils.say(ctx, f"Revoked case #{case_id}")

  async def _user_cases(self, ctx: ContextType, target: TargetType, active: bool | None) -> None:
    if ctx.guild is None:
      await utils.say(ctx, "You can't run that command here!")
      return

    if target == self.bot.user:
      await utils.say(ctx, "Nice try.")
      return

    database = case.get_database(ctx.guild.id)
    models = case.get_cases_for_user(database, target.id, active=active)

    if not models:
      await utils.say(ctx, "That user has no cases.")
      return

    if not self._has_moderation_perm(ctx):
      await utils.say(ctx, "You don't have permission.")
      return

    message = (
      f"Cases for <@{target.id}>:\n"
      + "\n".join(
        f"#{model.case_id} - {model.action.capitalize()}: "
        f"{'active' if model.active else 'inactive'}"
        for model in models
      )
    )

    await utils.say(ctx, message)

  # COMMANDS

  @commands.command()
  async def case(self, ctx: commands.Context, action: str, case_id: int | None = None) -> None:
    # we're effectively handling 
    # 2 commands in 1 function
    # because pycord doesn't know that 
    # `.case view` and `.case revoke` 
    # are separate commands.

    if action == "revoke":
      await self._revoke(ctx, case_id)
    elif action == "view":
      await self._case(ctx, case_id)
    else:
      await utils.say(
        ctx,
        f"View a case: `{prefix}case view <id>`\n"
        f"Revoke a case: `{prefix}case revoke <id>`"
      )

      return

  @case_group.command(name="view")
  async def slash_case(self, ctx: discord.ApplicationContext, case_id: int | None = None) -> None:
    await self._case(ctx, case_id)

  @case_group.command(name="revoke")
  async def slash_revoke(self, ctx: discord.ApplicationContext, case_id: int | None = None) -> None:
    await self._revoke(ctx, case_id)

  @commands.command()
  async def cases(self, ctx: commands.Context, target: TargetType) -> None:
    # luckily, we don't need to do anything stupid here.
    await self._user_cases(ctx, target, active=None)

  @commands.command()
  async def activecases(self, ctx: commands.Context, target: TargetType) -> None:
    await self._user_cases(ctx, target, active=True)

  @commands.command()
  async def inactivecases(self, ctx: commands.Context, target: TargetType) -> None:
    await self._user_cases(ctx, target, active=False)

  @discord.application_command(name="cases")
  async def slash_cases(self, ctx: discord.ApplicationContext, target: TargetType) -> None:
    await self._user_cases(ctx, target, active=None)

  @discord.application_command(name="activecases")
  async def slash_active_cases(self, ctx: discord.ApplicationContext, target: TargetType) -> None:
    await self._user_cases(ctx, target, active=True)

  @discord.application_command(name="inactivecases")
  async def slash_inactive_cases(self, ctx: discord.ApplicationContext, target: TargetType) -> None:
    await self._user_cases(ctx, target, active=False)

# FUNCTIONS

def setup(bot):
  bot.add_cog(CaseCommands(bot))