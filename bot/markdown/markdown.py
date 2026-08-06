#!/usr/bin/env python3
# bot/markdown/markdown.py

# IMPORTS

from pathlib import Path
from dataclasses import dataclass

# bolt

import bot.constants.toml as toml_config

# DATACLASSES

@dataclass(frozen=True)
class MarkdownFile:
  path: Path
  bot_name: str = toml_config.bot_name

  @property
  def find_and_replace(self) -> dict[str, str]:
    return {}

@dataclass(frozen=True)
class Help(MarkdownFile):
  path: Path = Path("bot/markdown/help.md")
  repo_link: str = toml_config.github_repo
  support_server_link: str = toml_config.support_server
  help_repo_message: str = toml_config.help_repo_message

  @property
  def find_and_replace(self) -> dict[str, str]:
    return {
      "{name}": self.bot_name,
      "{doc}": toml_config.help_documentation_link,
      "{support}": f"<{self.support_server_link}>",
      "{repo}": f"{self.help_repo_message}<{self.repo_link}>"
    }

@dataclass(frozen=True)
class Invite(MarkdownFile):
  path: Path = Path("bot/markdown/invite.md")
  invite_link: str = toml_config.invite_link
  support_server_link: str = toml_config.support_server

  @property
  def find_and_replace(self) -> dict[str, str]:
    return {
      "{name}": self.bot_name,
      "{invite}": f"<{self.invite_link}>",
      "{support}": f"<{self.support_server_link}>"
    }