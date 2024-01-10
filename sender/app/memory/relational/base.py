from sender.app.logging.sender_logging import DATABASE_LOGGER, INFO
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class DatabaseManager:
    __name__ = "DatabaseManager"

    def __repr__(self):
        return f"{self.__name__}Object - ({id(self)})"

    def __init__(self, engine, **options):
        self.engine: AsyncEngine = engine
        self.Session = async_sessionmaker(bind=self.engine)
        DATABASE_LOGGER.log(msg=f"{self.__name__} was successfully launched with {options}", level=INFO)

