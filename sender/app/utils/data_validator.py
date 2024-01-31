from typing import Dict, Union


class InputValidator:

    def __repr__(self):
        return f"InputValidatorObject - ({id(self)})"

    async def is_chat_username(self, username: str) -> bool:
        return username.startswith("@")

    async def try_parse(self, chat: Union[str, int]) -> Union[int, str]:
        from loader import sender

        response: Dict = {
            "chat_id": 0,
            "chat_name": ""
        }

        if await self.is_chat_username(chat):
            chat = await sender.bot.get_entity(chat)
            response["chat_id"] = chat.id
            response["chat_name"] = chat.title

        else:
            chat = int(chat)
            response["chat_id"] = chat
            response["chat_name"] = await sender.get_chat_name(chat)

        return response

