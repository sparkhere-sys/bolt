#!/usr/bin/env python3
# bot/markdown/markdown.py
'''
This file is paired with the .md files in `bot/markdown`.
'''

# LIBRARIES AND MODULES

from pathlib import Path
from dataclasses import dataclass, field

# pypkg

import bot.constants.toml as toml_config

# DATA CLASSES

'''
format:
* path: Path = Path("bot/markdown/FILE.md")
* other variables as needed, with type annotations
* find_and_replace: dict = {"find": "replace"}
'''
# also this isn't a docstring ^^^
# thats just a multi-line comment.

# this can be cleaner, but eh.

@dataclass(frozen=False)
class Help:
  '''
  Dataclass for the help markdown file.
  '''

  path: Path = Path("bot/markdown/help.md")
  repo_link: str = toml_config.github_repo
  support_server_link: str = toml_config.support_server
  help_repo_message: str = toml_config.help_repo_message

  find_and_replace: dict = field(default_factory=dict)
  
  def __post_init__(self): # this is the only way the find_and_replace dict can work. and i dont even need it to be mutable
    '''
    Runs after the dataclass is initialized to populate the find_and_replace dictionary.

    ### Parameters
    self: the instance of the Help dataclass.

    ### Returns
    nothing.

    ### Raises
    nothing.
    '''

    if not self.find_and_replace:
      self.find_and_replace.update({
        "{prefix}": toml_config.prefix,
        "{support}": f"<{self.support_server_link}>",
        "{repo}": f"{self.help_repo_message}<{self.repo_link}>",
      })

@dataclass(frozen=False)
class Invite:
  '''
  Dataclass for the invite markdown file.
  '''

  path: Path = Path("bot/markdown/invite.md")
  invite_link: str = toml_config.invite_link
  support_server_link: str = toml_config.support_server

  find_and_replace: dict = field(default_factory=dict)

  def __post_init__(self):
    '''
    Runs after the dataclass is initialized to populate the find_and_replace dictionary.

    ### Parameters
    self: the instance of the Invite dataclass.

    ### Returns
    nothing.

    ### Raises
    nothing.
    '''

    if not self.find_and_replace:
      self.find_and_replace.update({
        "{invite}": f"<{self.invite_link}>",
        "{support}": f"<{self.support_server_link}>",
      })
