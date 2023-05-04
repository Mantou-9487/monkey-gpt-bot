import re

from disnake import ApplicationCommandInteraction,AllowedMentions
from src.bot import Bot
from disnake.ext import commands
from src.conversation import Conversation, Question

class GPT(commands.Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Gpt Ready!")

    @commands.slash_command(name="gpt", description="詢問ChatGPT問題")
    async def gpt(self, interaction: ApplicationCommandInteraction,prompt:str):
      await interaction.response.defer()
      response = await self.bot.conversation.ask(Question(prompt))
      await interaction.followup.send(f"{interaction.user.mention} {response}")

def setup(bot):
    bot.add_cog(GPT(bot))
