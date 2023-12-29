from typing import Union
from telethon import TelegramClient
from telethon.types import Message, TypeInputPeer
from telethon.tl.functions.messages import GetHistoryRequest


class MessageParser:
    """
    MessageParser is a service that is used to parse messages data from private channel
    """

    def __repr__(self):
        return f"MessageParserObject - ({id(self)})"

    def __init__(self, bot: TelegramClient):
        self.__bot = bot

    async def parse_chat(self, channel_id: Union[str, int, TypeInputPeer], offset: int = 0, limit: int = 100) -> list[Message]:
        if not self.__bot.is_connected():
            await self.__bot.connect()

        history = await self.__bot(GetHistoryRequest(
            peer=channel_id,
            offset_id=offset,
            limit=limit,
            offset_date=None,
            add_offset=0,
            max_id=0,
            min_id=0,
            hash=0)
        )

        messages: list[Message] = [message for message in history.messages if isinstance(message, Message)]
        await self.__bot.disconnect()
        return messages

    async def parse_last_post(self, channel_id: Union[str, int, TypeInputPeer]):
        return await self.parse_chat(channel_id, limit=1)
