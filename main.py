from sender.app.services.parser import MessageParser
from sender.app.schemas.models import MessageToSend
from sender.app.api.api import api_router
from sender.app.config.bot import Sender
from fastapi import FastAPI
from settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_STR}/openapi.json',
    debug=settings.DEBUG_MODE
)

app.include_router(api_router, prefix=settings.API_STR)
sender = Sender()


@app.get("/")
async def root():
    result = await sender.copy(channel_id=2092585408)
    result = [MessageToSend(i) for i in result]
    await sender.paste(channel_id=2013085137, messages=result)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


