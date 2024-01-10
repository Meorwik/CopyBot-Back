from telethon.types import Message, Photo
from typing import Optional, Union
from pydantic import BaseModel


class MessageToSend(BaseModel):
    text: str = ""
    photo: Optional[Union[Photo, str]] = None
    base_message: Message

    class Config:
        arbitrary_types_allowed = True
