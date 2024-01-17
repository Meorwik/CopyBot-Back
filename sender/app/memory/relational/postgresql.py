from sqlalchemy.sql import select, delete, update
from sqlalchemy import Column, String, Integer
from .base import DatabaseManager
from .base import Base


class Redirects(Base):
    __tablename__ = 'redirects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    copy_from = Column(String, nullable=False)
    copy_from_name = Column(String, nullable=False)
    copy_to_name = Column(String, nullable=False)
    copy_to = Column(String, nullable=False)

    def __repr__(self):
        return f"Перенаправление из [({self.copy_from_name}) - ({self.copy_from})] в [({self.copy_to_name}) - ({self.copy_to})] "


class PostgresManager(DatabaseManager):
    __name__ = "PostgresManager"

    async def init(self):
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def get_all_redirects(self):
        async with self.Session() as session:
            query = select(Redirects)
            result = await session.execute(query)
            return result.fetchall()

    async def remove_all_redirects(self):
        async with self.Session() as session:
            query = delete(Redirects)
            await session.execute(query)
            await session.commit()
        return True

    async def add_redirect(self, redirect: Redirects) -> bool:
        async with self.Session() as session:
            session.add(redirect)
            await session.commit()
        return True

    async def update_redirect(self, redirect_id: int, redirect: Redirects):
        async with self.Session() as session:
            query = update(Redirects).where(Redirects.id == redirect_id).values(
                copy_from=redirect.copy_from,
                copy_to=redirect.copy_to,
                copy_from_name=redirect.copy_from_name,
                copy_to_name=redirect.copy_to_name
            )
            await session.execute(query)
            await session.commit()
        return True

    async def remove_redirect(self, redirect_id):
        async with self.Session() as session:
            delete_query = delete(Redirects).where(Redirects.id == redirect_id)
            await session.execute(delete_query)
            await session.commit()
        return True
