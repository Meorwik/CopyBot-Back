from sender.app.services.parsers.message_parser import MessageParser
from telethon.types import Message, TypeInputPeer
from ..schemas.models import MessageToSend
from telethon import TelegramClient
from settings import settings
from typing import Union


class BotManager:
    """
    This class must have one and only instance, system doesn't provide possibility where 2 bots with the same configs
    are created.

    This class also provides tools for managing main bot (engine in system context)
    """

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

    async def connect_to_bot(self):
        if not self.__bot.is_connected():
            await self.__bot.connect()

    async def disconnect_from_bot(self):
        await self.__bot.disconnect()

    @property
    def bot(self):
        return self.__bot


class Sender:
    """
    This class is the main structure in senderBot V - 1.0.0
    This class represents sender entity that provides main range of tools such as 'copy' and 'paste' from chat to chat
    """

    def __repr__(self):
        return f"SenderObject - ({id(self)})"

    def __init__(self):
        self.__bot_manager = BotManager()
        self.__bot = self.__bot_manager.bot

    @property
    def bot(self):
        return self.__bot

    async def init(self):
        await self.__bot_manager.init()

    async def connect_to_bot(self):
        await self.__bot_manager.connect_to_bot()

    async def disconnect_from_bot(self):
        await self.__bot_manager.disconnect_from_bot()

    async def convert_id_to_peer(self, chat_id: Union[int, str]) -> TypeInputPeer:
        chat_id: int = int(chat_id)
        return await self.__bot.get_input_entity(chat_id)

    async def get_chat_name(self, chat: Union[TypeInputPeer, str, int]) -> str:
        if isinstance(chat, Union[int, str]):
            chat = await self.convert_id_to_peer(chat)

        chat = await self.__bot.get_entity(chat)
        return chat.title

    async def paste(self, chat_id: Union[str, int], messages: list[MessageToSend]) -> bool:
        successfully_sent: int = 0
        chat: TypeInputPeer = await self.convert_id_to_peer(chat_id)
        await self.connect_to_bot()
        for message in messages:
            if message.photo is not None:
                await self.__bot.send_file(chat, message.photo, caption=message.text)

            else:
                await self.__bot.send_message(chat, message.text)
            successfully_sent += 1

        await self.disconnect_from_bot()
        return True if successfully_sent > len(messages) - 5 else False

    async def copy(self, chat_id: Union[str, int], **kwargs: dict[str: Union[str, int]]) -> list[Message]:
        parser = MessageParser(self.__bot)
        await self.connect_to_bot()
        chat: TypeInputPeer = await self.convert_id_to_peer(chat_id)
        messages: list[Message] = await parser.parse_chat(chat, kwargs=kwargs)
        await self.disconnect_from_bot()
        return messages

