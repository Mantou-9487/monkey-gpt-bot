import asyncio
import re
import os

from disnake import Message, Game, Status
from disnake.abc import Messageable
from disnake.ext.commands import InteractionBot

from .conversation import Conversation, ConversationStatus, Question


async def keep_typing(channel: Messageable):
    while True:
        await channel.trigger_typing()
        await asyncio.sleep(10)


class Bot(InteractionBot):
    def __init__(self, conversation: Conversation, *args, **kwargs):
        """
        :param conversation: Conversation instance
        :param args: args
        :param kwargs: kwargs
        """
        super().__init__(*args, **kwargs)

        self.conversation = conversation

        self.conversation.start_asking_loop(self.loop)

    async def on_ready(self):
        if self.conversation.status != ConversationStatus.PREPARED:
            await self.change_presence(activity=Game("準備中"), status=Status.dnd)

            await self.conversation.prepare()

            await self.change_presence(activity=Game("待命中"), status=Status.online)

            for file in os.listdir('./cogs'):  # 抓取所有cog資料夾裡的檔案
                if file.endswith('.py'):  # 判斷檔案是否是python檔
                    try:
                        # 載入cog,[:-3]是字串切片,為了把.py消除
                        self.load_extension(f'cogs.{file[:-3]}')
                        print(f'✅ 已加載 {file}')
                    except Exception as error:  # 如果cog未正確載入
                        print(f'❌ {file} 發生錯誤  {error}')
                        
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        if message.author.id == self.user.id:
            return

        if self.user not in message.mentions:
            return

        typing_task = self.loop.create_task(keep_typing(message.channel))

        prompt = re.sub(r'<@([0-9]+)>', "", message.content)

        response = await self.conversation.ask(Question(prompt))

        typing_task.cancel()

        await message.reply(response)