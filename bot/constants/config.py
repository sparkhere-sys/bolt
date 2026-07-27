#!/usr/bin/env python3
# bot/constants/config.py
# i know the name is weird but if it aint broke dont fix it. -spark

# IMPORTS

from pathlib import Path

# CONSTANTS

env_path = Path(".env")

default_prefix = "."

units = {
  "w": 86400 * 7, # weeks
  "d": 86400,     # days
  "h": 3600,      # hours
  "m": 60,        # minutes
  "s": 1          # seconds
}