import os

from settings import settings
from typing import Union, Final
from telethon.tl.types import Photo
from requests import post
from ..config.bot import BotManager
import base64
from io import BytesIO
from PIL import Image


class WatermarkRemover:
    __api_reference: Final[str] = settings.WATERMARK_REMOVER_API
    __api_token: Final[str] = settings.WATERMARK_REMOVER_TOKEN
    __temp_for_media: Final[str] = settings.TEMP_FOLDER_FOR_MEDIA
    __height_max_pixels: Final[int] = 1024
    __width_max_pixels: Final[int] = 1024

    __name__ = "WatermarkRemover"

    def __repr__(self):
        return f"{self.__name__}Object ---> ({id(self)})"

    async def __download_photo(self, image: Photo):
        bot_manager = BotManager()
        await bot_manager.connect_to_bot()
        file = await bot_manager.bot.download_media(image, self.__temp_for_media)
        await bot_manager.disconnect_from_bot()
        return file

    async def __resize_photo(self, image):
        image = Image.open(image)
        width, height = image.size

        if width > self.__width_max_pixels:
            width = self.__width_max_pixels

        if height > self.__height_max_pixels:
            height = self.__height_max_pixels

        resized_image = image.resize((width, height))
        return resized_image

    async def __encode_image(self, file) -> str:
        buffered = BytesIO()
        file.save(buffered, format="JPEG")

        base64_string = base64.b64encode(buffered.getvalue()).decode()
        return base64_string

    async def __remove_watermark(self, base64_string: str) -> str:
        data = """{
          \"image_file\": \"%s\",
          \"extra\": {
            \"response_image_type\": \"png\",
            \"enterprise_plan\": {
              \"enabled\": false
            }
          }
        }""" % base64_string

        headers = {
            'Authorization': self.__api_token,
            'Content-Type': 'application/json'
        }

        response = post(self.__api_reference, headers=headers, data=data)
        return response.json()

    async def __decode_image(self, base64_string):
        print(base64_string)

    async def remove_watermark(self, image: Photo):
        file = await self.__download_photo(image)
        resized_file = await self.__resize_photo(file)
        encoded_image = await self.__encode_image(resized_file)
        os.remove(file)

        encoded_image_no_watermark = await self.__remove_watermark(encoded_image)
        decoded_image = await self.__decode_image(encoded_image_no_watermark)
        return decoded_image

