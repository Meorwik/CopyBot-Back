from typing import Final
from os import environ

DEBUG_ON: Final[bool] = True
DEBUG_OFF: Final[bool] = False

API_ID: str = environ.get("API_ID")
API_HASH: str = environ.get("API_HASH")
TG_USERNAME: str = environ.get("TG_USERNAME")


class Settings:
    API_STR: str = '/api'
    PROJECT_NAME: str = 'sender'
    API_ID: str = API_ID
    API_HASH: str = API_HASH
    DEBUG_MODE: bool = DEBUG_ON
    TG_USERNAME: str = TG_USERNAME


settings = Settings()
