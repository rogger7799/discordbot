from discord.ext import commands
import discord
from discord import app_commands
from cogs.pollview import PollView
import typing
import datetime

class poll(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print("poll cog loaded successfully")

  @app_commands.command(name="poll", description="Make a poll!")
  async def poll(self, interaction: discord.Interaction, title: str, choices: str, context: typing.Optional[str]):
    
    
    # await interaction.response.defer()
    choices_list = [x.strip() for x in choices.split(',')]
    choices_len = len(choices_list)

    if choices_len < 2:
      embed = discord.Embed(title="Requires at least two options to make a poll!")
      await interaction.response.send_message(embed=embed, ephemeral=True)

    assert interaction.guild is not None
    member_num = interaction.guild.member_count
    
    embed = discord.Embed(
      title=title,
      description=f"0/{member_num} member have vote",
      color=discord.Color.pink()
    )
    
    embed.add_field(name="", value=context)
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
    embed.timestamp = datetime.datetime.utcnow()

    view = PollView(title, choices_len, choices_list, embed)

    await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
  await bot.add_cog(poll(bot), guilds=[discord.Object(id=guild_id)])
