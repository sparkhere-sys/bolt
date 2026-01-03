#!/usr/bin/python3
# bot/cogs/animal.py

# LIBRARIES AND MODULES

from io import BytesIO
import requests

## pycord

from discord.ext import commands
import discord

# pypkg

import bot.utils as utils
import bot.console as console


# ANIMAL CLASSES


class Bunny(commands.Cog):
  '''
  handles the bunny command(s)
  '''

  def __init__(self, bot):
    self.bot = bot

  async def _bunny(self, ctx):
    user = ctx.author

    api = "https://rabbit-api-two.vercel.app/api/random"
    data = requests.get(api).json()

    image_url = data["url"]
    response = requests.get(image_url)

    image = BytesIO(response.content)
    image.seek(0)

    console.log(f"bnuy image requested by {user} ({user.id})", "LOG")

    await utils.say(ctx, file=discord.File(image, filename="image.png"))

  # COMMANDS

  @commands.command()
  async def bunny(self, ctx):
    await self._bunny(ctx)

  @commands.slash_command(name="bunny", description="sends a random bunny image")
  async def slash_bunny(self, ctx):
    await self._bunny(ctx)



class Dog(commands.Cog):
  '''
  handles the dog command(s)
  '''

  def __init__(self, bot):
    self.bot = bot

  async def _dog(self, ctx):
    user = ctx.author

    api = "https://dog.ceo/api/breeds/image/random"
    data = requests.get(api).json()

    image_url = data["message"]
    response = requests.get(image_url)

    image = BytesIO(response.content)
    image.seek(0)

    console.log(f"Dog image requested by {user} ({user.id})", "LOG")

    await utils.say(ctx, file=discord.File(image, filename="image.png"))

  # COMMANDS

  @commands.command()
  async def dog(self, ctx):
    await self._dog(ctx)

  @commands.slash_command(name="dog", description="sends a random dog image")
  async def slash_dog(self, ctx):
    await self._dog(ctx)



class Cat(commands.Cog):
  '''
  handles the cat command(s)
  '''

  def __init__(self, bot):
    self.bot = bot

  async def _cat(self, ctx):
    user = ctx.author

    catapi = "https://cataas.com/cat"
    response = requests.get(catapi)
    image = BytesIO(response.content)
    image.seek(0)

    console.log(f"Cat image requested by {user} ({user.id})", "LOG")

    await utils.say(ctx, file=discord.File(image, filename="image.png"))

  # COMMANDS

  @commands.command()
  async def cat(self, ctx):
    await self._cat(ctx)

  @commands.slash_command(name="cat", description="sends a random cat image")
  async def slash_cat(self, ctx):
    await self._cat(ctx)



class Duck(commands.Cog):
  '''
  handles the duck command(s)
  '''

  def __init__(self, bot):
    self.bot = bot

  async def _duck(self, ctx):
    user = ctx.author

    api = "https://random-d.uk/api/random"
    data = requests.get(api).json()

    image_url = data["url"]
    response = requests.get(image_url)

    image = BytesIO(response.content)
    image.seek(0)

    console.log(f"Duck image requested by {user} ({user.id})", "LOG")

    await utils.say(ctx, file=discord.File(image, filename="image.png"))

  # COMMANDS

  @commands.command()
  async def duck(self, ctx):
    await self._duck(ctx)

  @commands.slash_command(name="duck", description="sends a random duck image")
  async def slash_duck(self, ctx):
    await self._duck(ctx)



class Fox(commands.Cog):
  '''
  handles the fox command(s)
  '''

  def __init__(self, bot):
    self.bot = bot

  async def _fox(self, ctx):
    user = ctx.author

    api = "https://randomfox.ca/floof/"
    data = requests.get(api).json()

    image_url = data["image"]
    response = requests.get(image_url)

    image = BytesIO(response.content)
    image.seek(0)

    console.log(f"fox image requested by {user} ({user.id})", "LOG")

    await utils.say(ctx, file=discord.File(image, filename="image.png"))

  # COMMANDS

  @commands.command()
  async def fox(self, ctx):
    await self._fox(ctx)

  @commands.slash_command(name="fox", description="sends a random fox image")
  async def slash_fox(self, ctx):
    await self._fox(ctx)

  def setup(bot):
    '''
    adds all the commands to the bot
    '''

    bot.add_cog(Bunny(bot))
    bot.add_cog(Fox(bot))
    bot.add_cog(Dog(bot))
    bot.add_cog(Duck(bot))
    bot.add_cog(Cat(bot))