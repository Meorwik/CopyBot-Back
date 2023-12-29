from telethon.types import TypeInputPeer, Message
from ..services.parser import MessageParser
from ..schemas.models import MessageToSend
from telethon import TelegramClient
from settings import settings
from typing import Union


class BotManager:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BotManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__bot = TelegramClient(
            session=settings.TG_USERNAME,
            api_id=settings.API_ID,
            api_hash=settings.API_HASH,
        )

    @property
    def bot(self):
        return self.__bot


class Sender:
    def __repr__(self):
        return f"SenderObject - ({id(self)})"

    def __init__(self):
        self.__bot_manager = BotManager()
        self.__bot = self.__bot_manager.bot

    async def paste(self, channel_id: Union[str, int, TypeInputPeer], messages: list[MessageToSend]):
        for message in messages:
            await self.__bot.send_message(channel_id, message)

    async def copy(self, channel_id: Union[str, int, TypeInputPeer], offset: int = 0, limit: int = 100) -> list[Message]:
        parser = MessageParser(self.__bot)
        return await parser.parse_last_post(channel_id)


