#!/usr/bin/env python3

# IMPORTS

import peewee
from pathlib import Path

## bolt

from bot.cogs.moderation.types import Case

# CONSTANTS

db_path = Path("data/cases.db")
db_path.parent.mkdir(parents=True, exist_ok=True)

db = peewee.SqliteDatabase(str(db_path)) # pylance stop torturing me

# CLASSES

class BaseModel(peewee.Model):
  class Meta:
    database = db

class CaseModel(BaseModel):
  class Meta:
    table_name = "cases"

  case_id = peewee.AutoField()
  active = peewee.BooleanField(default=True)

  action = peewee.CharField()
  target = peewee.BigIntegerField()
  moderator = peewee.BigIntegerField()
  reason = peewee.TextField()
  duration = peewee.CharField(null=True)
  guild = peewee.BigIntegerField()

  created_at = peewee.DateTimeField()
  expires_at = peewee.DateTimeField(null=True)

  @classmethod
  def from_case(cls, case: Case) -> "CaseModel": # type annotations are weird
    return cls(
      active=case.active,
      action=case.action.value.name,
      guild=case.guild.id,
      target=case.target.id,
      moderator=case.moderator.id,
      reason=case.reason,
      created_at=case.created_at,
      expires_at=case.expires_at,
      duration=case.duration,
    )

  # the conversion to a db entry is one-way

# FUNCTIONS

def init_database():
  db.connect(reuse_if_open=True)
  db.create_tables([CaseModel])