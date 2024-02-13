from ..schemas.models import MessageToSend
from telethon.types import Message


class MessageTransformer:
    """
    This class automatically transforms 'Message' arrays into array of 'MessageToSend' model objects
    """

    def __init__(self):
        self.__current_model = MessageToSend

    async def transform_to_current_model(self, messages: list[Message]) -> list:
        transformed_messages = [
            self.__current_model(
                text=message.message,
                media=message.media
            )
            for message in messages
        ]

        return transformed_messages[::-1]


