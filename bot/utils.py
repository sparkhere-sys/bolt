# bot/utils.py

# FUNCTIONS

async def say(ctx, msg, is_slash=False, ephemeral=False):
  if is_slash:
    await ctx.respond(msg, ephemeral=ephemeral)
  else:
    await ctx.send(msg)