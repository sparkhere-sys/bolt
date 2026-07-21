#!/usr/bin/env python3

# IMPORTS

try:
  from colorama import init
except ImportError:
  allow_colors = False
else:
  allow_colors = True
  init()

from enum import Enum

# FUNCTIONS

def hex_to_rgb(hex: str) -> tuple[int, int, int]:
  hex = hex.lstrip("#")
  return (
    int(hex[0:2], 16),
    int(hex[2:4], 16),
    int(hex[4:6], 16)
  )

def rgb_fg(r: int, g: int, b: int) -> str:
  if not allow_colors:
    return ""

  return f"\033[38;2;{r};{g};{b}m"

def rgb_bg(r: int, g: int, b: int) -> str:
  if not allow_colors:
    return ""
  
  return f"\033[48;2;{r};{g};{b}m"

def fg(hex: str) -> str:
  r, g, b = hex_to_rgb(hex)
  return rgb_fg(r, g, b)

def bg(hex: str) -> str:
  r, g, b, = hex_to_rgb(hex)
  return rgb_bg(r, g, b)

# ENUMS

class LogLevel(Enum):
  LOG   = ("#cdd6f4", "#313244")
  DEBUG = ("#89dceb", "#11111b")
  INFO  = ("#89b4fa", "#11111b")
  WARN  = ("#f9e2af", "#11111b")
  ERROR = ("#f38ba8", "#11111b")
  FATAL = ("#cba6f7", "#11111b")
  READY = ("#a6e3a1", "#11111b")

  @property
  def color(self) -> str:
    bg_hex, fg_hex = self.value
    return bg(bg_hex) + fg(fg_hex)
  
  @property
  def badge(self) -> str:
    return f"{self.color} {self.name:^7} {reset}"

# CONSTANTS

reset = "\033[0m"
dim = fg("#313244")