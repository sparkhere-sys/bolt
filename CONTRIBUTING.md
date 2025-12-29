# Contributing

## Style Guide

~~basically PEP 8 but scuffed~~

* Use 2 spaces for indentation
* Class names are in `PascalCase`
* Variable names and function names are in `snake_case`
* All variable names should be lowercase, including constants.
* Section headers should be in all caps.

If you don't like the styling of Bolt, no problem! You can code in your own style and a contributor can restyle your code to fit Bolt.

### Section headers

```py
#!/usr/bin/python3
# path/to/file.py

# LIBRARIES AND MODULES

import smth_from_stdlib

## pycord

import discord

## pypkg

import bot.module.inside.bolt

# CLASSES

class PlaceholderClass:
  pass

# FUNCTIONS

def placeholder_function():
  pass
```

## Etiquette

* When working on Bolt, create your own branch and name it `yourname-pr`.
* Don't commit directly to `main`, use pull requests instead.
* Don't mess with other people's branches, leave them be.
* Don't be a dick.

---

Thanks for contributing!