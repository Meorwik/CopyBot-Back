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

    async def __validate_chat_id(self, chat_id: Union[str, int]) -> bool:
        from loader import sender

        if isinstance(chat_id, str):
            if chat_id.isnumeric():
                chat_id = int(chat_id)
            else:
                return False

        peer = await sender.convert_id_to_peer(chat_id)
        chat = await sender.bot.get_entity(peer)
        return bool(chat)

    async def __validate_chat_username(self, username: str) -> bool:
        from loader import sender
        return bool(await sender.bot.get_entity(username))

    async def validate_chat(self, chat_hint: Union[str, int]) -> bool:
        if await self.is_chat_username(chat_hint):
            return await self.__validate_chat_username(chat_hint)

        else:
            return await self.__validate_chat_id(chat_hint)

