from loader import sender, postgres_manager, scheduler, message_transformer
from sender.app.memory.relational.postgresql import Redirects
from sender.app.api.api import api_router
from settings import settings
from fastapi import FastAPI
from telethon import events
from typing import List


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_STR}/openapi.json',
    debug=settings.DEBUG_MODE
)

app.include_router(api_router, prefix=settings.API_STR)


async def check_updates():
    redirects: List[Redirects] = await postgres_manager.get_all_redirects()
    if redirects:
        await sender.connect_to_bot()
        copy_from = [await sender.convert_id_to_peer(redirect[0].copy_from) for redirect in redirects]

        @sender.bot.on(events.NewMessage(chats=copy_from))
        async def handle_updates(event: events.NewMessage.Event):
            for redirect in redirects:
                if str(event.chat.id) == str(redirect[0].copy_from):
                    message_to_send = await message_transformer.transform_to_current_model([event.message])
                    await sender.paste(redirect[0].copy_to, message_to_send)

    else:
        return False


@app.on_event("startup")
async def startup_event():
    await postgres_manager.init()
    await scheduler.start()
    await sender.init()
    scheduler.add_job(check_updates, "interval", seconds=10)


@app.get("/")
async def root():
    return {
        str(key + 1): str(value)
        for key, value
        in enumerate(await postgres_manager.get_all_redirects())
    }


