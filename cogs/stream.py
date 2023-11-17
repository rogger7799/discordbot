import discord
from discord.ext import commands
import requests
import json


class stream(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print("stream cog loaded successfully")

  @commands.command()
  async def stream(self, ctx):
    try:
      r = requests.get(url)
    except Exception as e:
      print(e)

    data = r.json()
    is_live = data["live"]
    vid_url = data["vidi"]

    await ctx.defer(ephemeral=True)
    
    if is_live == "live":
      await ctx.send("live")

    elif is_live == "upcoming":
      await ctx.send("upcoming")

    else:
      await ctx.send("latest stream")

    await ctx.send(vid_url)


async def setup(bot):
  await bot.add_cog(stream(bot))
