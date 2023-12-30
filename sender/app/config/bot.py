from telethon.types import TypeInputPeer, Message
from ..services.parser import MessageParser
from ..schemas.models import MessageToSend
from telethon import TelegramClient
from telethon.hints import Entity
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

    async def init(self):
        self.__bot = await self.bot.start()

    @property
    def bot(self):
        return self.__bot


class Sender:
    def __repr__(self):
        return f"SenderObject - ({id(self)})"

    def __init__(self):
        self.__bot_manager = BotManager()
        self.__bot = self.__bot_manager.bot

    async def init(self):
        await self.__bot_manager.init()

    async def connect_to_bot(self):
        if not self.__bot.is_connected():
            await self.__bot.connect()

    async def disconnect_from_bot(self):
        await self.__bot.disconnect()

    async def paste(self, channel_id: Union[str, int, TypeInputPeer, Entity], messages: list[MessageToSend]):
        channel = await self.__bot.get_entity(channel_id)
        for message in messages:
            await self.__bot.send_message(channel, message.text)

    async def copy(self, channel_id: Union[str, int, TypeInputPeer, Entity], offset: int = 0, limit: int = 100) -> list[Message]:
        await self.connect_to_bot()
        parser = MessageParser(self.__bot)
        channel = await self.__bot.get_input_entity(channel_id)
        messages: list[Message] = await parser.parse_last_post(channel)
        await self.disconnect_from_bot()
        return messages


