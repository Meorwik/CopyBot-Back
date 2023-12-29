from pydantic import BaseModel
from telethon.types import Message
from typing import Union


class MessageToSend(BaseModel):
    text: str
    picture: str

    def __init__(self, message: Message):
        super().__init__()
        self.text = message.message
        self.picture = message.media.photo

#
# class SenderConfig(BaseModel):
#     messages: list[Union[Message, MessageToSend]]
#     timeout: int = 30
#     channel_to: Union[str, int]
#     channel_from: Union[str, int]
#