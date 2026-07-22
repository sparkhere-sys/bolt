#!/usr/bin/env python3

# IMPORTS

from typing import Union

## pycord

import discord
from discord.ext import commands

# CONSTANTS

ContextType = Union[commands.Context, discord.ApplicationContext]
TargetType = Union[discord.User, discord.Member]