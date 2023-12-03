import discord
from discord.interactions import InteractionMessage
import discord.ui
from collections import defaultdict



class PollButton(discord.ui.Button):

  def __init__(self, button_label: str, idx: int):
    super().__init__(style=discord.ButtonStyle.primary, label=button_label)
    self.button_label = button_label
    self.idx = idx

  async def callback(self, interaction: discord.Interaction):
    assert self.view is not None
    view: PollView = self.view
  
    if (interaction.user.id not in view.voter):
      view.choices_counter[self.idx].append(interaction.user.mention)
      view.votes_counter += 1

      assert interaction.guild is not None
      member_num = interaction.guild.member_count
      
      embed = view.embed
      embed.description = f"{view.votes_counter}/{member_num} member have voted"
    
      await interaction.response.edit_message(embed=embed, view=view)
      
      embed = discord.Embed(
        title="Vote successfully!",
        description=f"You have voted to {self.label}!",
        color=discord.Color.green())

      await interaction.followup.send(embed=embed, ephemeral=True)
      view.voter[interaction.user.id] = self.label

    else:
      embed = discord.Embed(
        title="Vote failed!",
        description=f"You have already voted to {view.voter[interaction.user.id]}!",
        color=discord.Color.red())

      await interaction.response.send_message(embed=embed, ephemeral=True)
  
    
class PollCountButton(discord.ui.Button):

  def __init__(self):
    super().__init__(style=discord.ButtonStyle.green, label="Counting")

  async def callback(self, interaction: discord.Interaction):
    assert self.view is not None
    view: PollView = self.view
    
    embed = discord.Embed(title=view.title,
                          description=f"total {view.votes_counter} voters",
                          color=discord.Color.pink())
    embed.set_author(name=interaction.user.name,
                     icon_url=interaction.user.display_avatar)

    for idx, choice in enumerate(view.choices_list):
      embed.add_field(name=choice,
                      value="".join(view.choices_counter[idx]),
                      inline=False)
    
    await interaction.response.send_message(embed=embed)


class PollView(discord.ui.View):

  def __init__(self, title: str, choices_len: int, choices_list: list[str], embed: discord.Embed):
    super().__init__()
    self.title = title
    self.choices_list = choices_list
    self.choices_counter = [[] for i in range(choices_len)]
    self.voter = defaultdict()
    self.votes_counter = 0
    self.button_disabled = False
    self.embed = embed

    for i in range(choices_len):
      self.add_item(PollButton(choices_list[i], i))

    self.add_item(PollCountButton())

# Thin Pizza Crust,  Apple-Cheddar Panini,  Meatloaf
