import asyncio
from os import getenv
from dotenv import load_dotenv

from disnake import Intents
from revChatGPT.V1 import Chatbot

from src.bot import Bot
from src.conversation import Conversation, Question

config = {
  "email":getenv("email"),
  "password":getenv("password"),
  "access_token":getenv("access_token")

}

def main():
    conversation = Conversation(
        Chatbot(config=config),
        load_brainwash()
    )

    bot = Bot(conversation, intents=Intents.all())

    try:
        load_dotenv()
        bot.run(getenv("TOKEN"))
    except KeyboardInterrupt:
        conversation.close()

        asyncio.get_event_loop().close()


def load_brainwash() -> list[Question]:
    """
    Load brainwash messages from brainwash.txt
    :return: A list of Question
    """
    with open(getenv("BRAINWASH_PATH", "./brainwash.txt"), "r", encoding='utf-8') as f:
        return [Question(line) for line in f.readlines()]


if __name__ == "__main__":
    main()