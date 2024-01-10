from sender.app.memory.relational.postgresql import PostgresManager
from sender.app.core.logic import MessageTransformer
from sender.app.services.scheduler import Scheduler
from sender.app.config.bot import Sender
from settings import settings


postgres_manager = PostgresManager(settings.POSTGRES_ENGINE)
message_transformer = MessageTransformer()
scheduler = Scheduler()
sender = Sender()
