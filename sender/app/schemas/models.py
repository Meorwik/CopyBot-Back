from telethon.types import TLObject
from typing import Optional, Union
from pydantic import BaseModel


class MessageToSend(BaseModel):
    text: str = ""
    media: Optional[Union[TLObject]] = None

    class Config:
        arbitrary_types_allowed = True
