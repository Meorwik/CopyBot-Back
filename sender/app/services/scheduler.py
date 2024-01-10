from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Scheduler:
    """
    Scheduler for executing asynchronous tasks (TimeZone by default is UTC)
    """

    def __repr__(self):
        return f"SchedulerObject - ({id(self)})"

    def __init__(self):
        self.__engine = AsyncIOScheduler()

    def add_job(self, job, trigger: str, hours: int = 1):
        self.__engine.add_job(job, trigger=trigger, hours=hours)

    async def start(self):
        self.__engine.start()

