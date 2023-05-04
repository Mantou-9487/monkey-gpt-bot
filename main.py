import asyncio
from os import getenv
from dotenv import load_dotenv

from disnake import Intents
from revChatGPT.V1 import Chatbot

from src.bot import Bot
from src.conversation import Conversation, Question

config = {
  "email":"opcantel@gmail.com",
  "password":"ac2475axn0104",
  "access_token":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJvcGNhbnRlbEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci1EbkhHODNVdENhODdLTGNGVjBQU3pQUEcifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTAxOTQwMzk4NTY4MDMwMDA2MDE5IiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY4MzIwMDE2NiwiZXhwIjoxNjg0NDA5NzY2LCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9mZmxpbmVfYWNjZXNzIn0.kOCLkVA7zr5gUY__hf79NNGmuhiRd_e_zrC1yYPtry80pyVEHmntghwYA7UtHszrlJBWnElp6xQMFyLj-4viW56lB9KTNim7_sZfE4mfZYP4tYe23iQ18qO_Y9_2Iy2Run5LFLKHnCkl71tdE_IqhEx6DeW_vT7hapXl-2gYeNIRYENtq02xnxrUKeUTDHzha0pPwGrdj4gda5jlqmJel1FEEHutkrWp0tgrC9VkRgB_o50BdA8mwZlAxkwYDnHXisQlMHpwtNJZWfBO3O42QHPHszCtI022dSR-ik9_tPCI0uASGsCgiyeZ8rjnBMeo7Un2C_SJrGOejRQ-CtndAA"

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