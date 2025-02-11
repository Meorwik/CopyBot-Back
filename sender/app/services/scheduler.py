from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from datetime import datetime, timedelta
from redis.asyncio import Redis
from settings import settings
from typing import Dict, Final
from pytz import timezone
import asyncio


class Scheduler:
    """
    Scheduler for executing asynchronous tasks (TimeZone by default is UTC)
    """

    def __repr__(self):
        return f"SchedulerObject - ({id(self)})"

    def __setup_redis_job_store(self):
        jobs_key: Final[str] = 'apscheduler.jobs'
        run_times_key: Final[str] = "run_times_key"

        jobstores = {
            'default': RedisJobStore(
                jobs_key=jobs_key,
                run_times_key=run_times_key,
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD
            ),
        }
        return jobstores

    def __setup_job_defaults(self):
        job_defaults = {'misfire_grace_time': 5}
        return job_defaults

    def __setup_timezone(self):
        tz = timezone('Etc/GMT-6')
        return tz

    def __init__(self):
        jobstores: Dict = self.__setup_redis_job_store()
        job_defaults: Dict = self.__setup_job_defaults()
        scheduler_timezone = self.__setup_timezone()
        self.__engine: AsyncIOScheduler = AsyncIOScheduler(
            jobstores=jobstores,
            job_defaults=job_defaults,
            timezone=scheduler_timezone
        )

    def add_job(self, job, trigger: str, seconds: int):
        self.__engine.add_job(job, trigger=trigger, seconds=seconds, max_instances=1)

    async def start(self):
        self.__engine.start()

