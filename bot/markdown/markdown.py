#!/usr/bin/env python3
# bot/markdown/markdown.py
'''
paired with the md files in bot/markdown.
'''

# LIBRARIES AND MODULES

from pathlib import Path
from bot.constants.base import prefix
from dataclasses import dataclass, field

# pypkg

from bot.constants.toml import markdown

# DATA CLASSES

'''
format:
* path: Path = Path("bot/markdown/FILE.md")
* other variables as needed, with type annotations
* find_and_replace: dict = {"find": "replace"}
'''

# this can be cleaner, but eh.

@dataclass(frozen=False)
class Help:
  path: Path = Path("bot/markdown/help.md")
  repo_link: str = markdown["github_repo"]
  support_server_link: str = markdown["support_server"]
  help_repo_message: str = markdown["help_repo_message"]

  find_and_replace: dict = field(default_factory=dict)
  
  def __post_init__(self): # this is the only way the find_and_replace dict can work. and i dont even need it to be mutable
    if not self.find_and_replace:
      self.find_and_replace.update({
        "{prefix}": prefix,
        "{support}": f"<{self.support_server_link}>",
        "{repo}": f"{self.help_repo_message}<{self.repo_link}>",
      })

@dataclass(frozen=False)
class Invite:
  path: Path = Path("bot/markdown/invite.md")
  invite_link: str = markdown["invite_link"]
  support_server_link: str = markdown["support_server"]

  find_and_replace: dict = field(default_factory=dict)

  def __post_init__(self):
    if not self.find_and_replace:
      self.find_and_replace.update({
        "{invite}": f"<{self.invite_link}>",
        "{support}": f"<{self.support_server_link}>",
      })