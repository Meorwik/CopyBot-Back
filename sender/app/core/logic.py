from ..schemas.models import MessageToSend
from telethon.types import Message


class MessageTransformer:
    """
    This class automatically transforms 'Message' arrays into array of 'MessageToSend' model objects
    """

    __current_model = MessageToSend

    async def transform_to_current_model(self, messages: list[Message]) -> list[__current_model]:
        transformed_messages = [
            self.__current_model(
                base_message=message,
                text=message.message,
                photo=message.media.photo
            )
            if message.media is not None and message.media.photo is not None else
            self.__current_model(
                base_message=message,
                text=message.message,
            )
            for message in messages
        ]
        return transformed_messages[::-1]


