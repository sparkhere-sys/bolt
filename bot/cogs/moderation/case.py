#!/usr/bin/env python3

# IMPORTS

from __future__ import annotations
from pathlib import Path

import peewee

## bolt

from bot.cogs.moderation.types import Case
import bot.console as console

# FUNCTIONS

def get_database(guild_id: int) -> peewee.SqliteDatabase:
  db_path = Path("data") / str(guild_id) / "cases.db"
  db_path.parent.mkdir(parents=True, exist_ok=True)

  console.debug(f"Using database: {db_path}")
  return peewee.SqliteDatabase(str(db_path))

def init_database(database: peewee.SqliteDatabase):
  console.debug("Connecting...")
  database.connect(reuse_if_open=True)
  console.debug("Connected!")

  console.debug("Creating tables...")
  with database.bind_ctx([CaseModel]):
    database.create_tables([CaseModel])

  console.debug("Done!")

def get_case(database: peewee.SqliteDatabase, case_id: int) -> CaseModel | None:
  with CaseModel.bind_ctx(database):
    try:
      model = CaseModel.get_by_id(case_id)
    except peewee.DoesNotExist:
      console.debug(f"Case #{case_id} does not exist")
      return None

    console.debug(f"Found case #{case_id}")
    return model

def get_cases_for_user(database: peewee.SqliteDatabase, user_id: int, active: bool | None = None) -> list[CaseModel]:
  console.debug(f"Finding active={active} cases for user ID {user_id}")
  with CaseModel.bind_ctx(database):
    query = CaseModel.select().where(CaseModel.target == user_id)

    if active is not None:
      query = query.where(CaseModel.active == active)

    cases = list(query)

    console.debug(f"Found {len(cases)} cases")
    return cases

def revoke_case(database: peewee.SqliteDatabase, case_id: int) -> bool | None:
  console.debug(f"Revoking case #{case_id}...")
  with CaseModel.bind_ctx(database):
    try:
      case = CaseModel.get_by_id(case_id)
    except peewee.DoesNotExist:
      console.debug(f"Case #{case_id} does not exist")
      return None

    if not case.active:
      console.debug(f"Case #{case_id} is already inactive")
      return False

    case.active = False
    case.save()

    console.debug(f"Case #{case_id} revoked")
    return True

# CLASSES

class CaseModel(peewee.Model):
  class Meta:
    table_name = "cases"

  # fields

  case_id = peewee.AutoField()
  active = peewee.BooleanField(default=True)

  action = peewee.CharField()
  target = peewee.BigIntegerField()
  moderator = peewee.BigIntegerField()
  reason = peewee.TextField()
  duration = peewee.CharField(null=True)

  created_at = peewee.DateTimeField()
  expires_at = peewee.DateTimeField(null=True)

  # FUNCTIONS

  def __init__(self, database: peewee.SqliteDatabase | None = None, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.database = database

  def save(self, *args, **kwargs):
    if self.database is None:
      console.debug("No database bound")
      return super().save(*args, **kwargs)

    with self.bind_ctx(self.database):
      result = super().save(*args, **kwargs)

      console.debug(f"save() returned {result}")
      return result

  @classmethod
  def from_case(cls, case: Case) -> CaseModel:
    database = get_database(case.guild.id)
    init_database(database)

    return cls(
      database=database,
      active=case.active,
      action=case.action.value.name,
      target=case.target.id,
      moderator=case.moderator.id,
      reason=case.reason,
      created_at=case.created_at,
      expires_at=case.expires_at,
      duration=case.duration,
    )

  # the conversion to a db entry is one-way