import os
import asyncio
import datetime
import discord
from discord.ext import commands
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command()
async def load(ctx, extension):
  try:
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")
  except Exception as e:
    print(e)


@bot.command()
async def unload(ctx, extension):
  try:
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")
  except Exception as e:
    print(e)


@bot.command()
async def reload(ctx, extension):
  try:
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")
  except Exception as e:
    print(e)


@bot.command()
async def loadall(ctx):
  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      try:
        await bot.load_extension(f"cogs.{filename[:-3]}")
        await ctx.send(f"Loaded {filename[:-3]} done.")
      except Exception as e:
        print(e)


@bot.command()
async def unloadall(ctx):
  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      try:
        await bot.unload_extension(f"cogs.{filename[:-3]}")
        await ctx.send(f"UnLoaded {filename[:-3]} done.")
      except Exception as e:
        print(e)


@bot.event
async def on_ready():
  print(f"log in with {bot.user}")
  # channel_id = 1171821900134088855
  # channel = bot.get_channel(channel_id)
  # await channel.send("***bot is on!!!***")


@bot.event
async def on_member_join(member):
  at_time = get_time(+8)
  member_id = member.id
  member_name = member.name
  member_nick = member.nick
  print(f"[{member_name}]#[{member_nick}]has joined the server at {at_time}")

  data = {
      "action": "join",
      "name": member_name,
      "id": member_id,
      "nick": member_nick,
      "at_time": at_time
  }

  try:
    with open('serverlog.json', 'a') as f:
      json.dump(data, f)
  except Exception as e:
    print(e)
  

@bot.event
async def on_member_remove(member):
  at_time = get_time(+8)
  member_id = member.id
  member_name = member.name
  member_nick = member.nick
  print(f"[{member_name}]#[{member_nick}] has left the server at {at_time}")

  data = {
      "action": "leave",
      "name": member_name,
      "id": member_id,
      "nick": member_nick,
      "at_time": at_time
  }
  
  try:
    with open('serverlog.json', 'a') as f:
      json.dump(data, f)
  except Exception as e:
    print(e)


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
  await ctx.send("***shuting down...***")
  await ctx.bot.close()


@bot.command()
async def nowtime(ctx):
  await ctx.send(get_time(+8))


def get_time(utc_delta):
  time = datetime.datetime.now() + datetime.timedelta(hours=utc_delta)
  return time.strftime("%Y-%m-%d %H:%M:%S")

@bot.command(pass_context=True)
async def helpc(ctx):
  embed = discord.Embed(description='''**User Commands:**
        !helpc - Shows this message
        !nowtime - Displays the current time in utc+8
        !serverlog - Displays the server log
        ''')
  await ctx.send(embed=embed)


async def main():
  async with bot:
    await bot.start(
        "token"
    )

if __name__ == "__main__":
  asyncio.run(main())
