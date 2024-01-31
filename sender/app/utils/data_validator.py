from typing import Dict, Union


class InputValidator:

    def __repr__(self):
        return f"InputValidatorObject - ({id(self)})"

    async def is_chat_username(self, username: str) -> bool:
        username = str(username)
        return username.startswith("@")

    async def try_parse(self, chat: Union[str, int]) -> Dict:
        from loader import sender

        response: Dict = {
            "chat_id": 0,
            "chat_name": ""
        }

        if await self.is_chat_username(chat):
            chat = await sender.bot.get_entity(chat)
            response["chat_id"] = str(chat.id)
            response["chat_name"] = chat.title

        else:
            response["chat_id"] = str(chat)
            response["chat_name"] = await sender.get_chat_name(int(chat))

        return response

