from telethon.types import Photo
from typing import Optional, Union
from pydantic import BaseModel


class MessageToSend(BaseModel):
    text: str = ""
    photo: Optional[Union[Photo, str]] = None

    class Config:
        arbitrary_types_allowed = True
