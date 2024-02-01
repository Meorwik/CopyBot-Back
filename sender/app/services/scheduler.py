from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Scheduler:
    """
    Scheduler for executing asynchronous tasks (TimeZone by default is UTC)
    """

    def __repr__(self):
        return f"SchedulerObject - ({id(self)})"

    def __init__(self):
        self.__engine = AsyncIOScheduler()

    def add_job(self, job, trigger: str, seconds: int):
        self.__engine.add_job(job, trigger=trigger, seconds=seconds)

    async def start(self):
        self.__engine.start()

