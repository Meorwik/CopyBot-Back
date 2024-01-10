from telethon.tl.functions.messages import GetHistoryRequest
from telethon.types import Message, TypeInputPeer
from telethon import TelegramClient
from typing import Union


class MessageParser:
    """
    MessageParser is a service that is used to parse messages data from private channel
    """
    __name__ = "MessageParser"

    OFFSET_PARAM_NAME: str = "offset"
    LIMIT_PARAM_NAME: str = "limit"

    OFFSET_DEFAULT: int = 0
    LIMIT_DEFAULT: int = 100

    def offset_param_name(self) -> str:
        return self.OFFSET_PARAM_NAME

    def limit_param_name(self) -> str:
        return self.LIMIT_PARAM_NAME

    def __init__(self, bot: TelegramClient):
        self.__bot = bot

    async def parse_chat(self, chat: TypeInputPeer, **kwargs: dict[str: Union[str, int]]) -> list[Message]:
        offset: int = self.OFFSET_DEFAULT
        limit: int = self.LIMIT_DEFAULT
        kwargs = kwargs["kwargs"]
        if "kwargs" in kwargs:
            kwargs = kwargs["kwargs"]

        if self.OFFSET_PARAM_NAME in kwargs:
            offset: int = kwargs[self.OFFSET_PARAM_NAME]

        if self.LIMIT_PARAM_NAME in kwargs:
            limit: int = kwargs[self.LIMIT_PARAM_NAME]

        history = await self.__bot(
            GetHistoryRequest(
                peer=chat, offset_id=offset, limit=limit,
                offset_date=None, add_offset=0, max_id=0, min_id=0, hash=0)
        )

        messages: list[Message] = [
            message for message in history.messages if isinstance(message, Message)
        ]

        return messages
