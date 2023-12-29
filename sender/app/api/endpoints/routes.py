from fastapi import APIRouter

router = APIRouter()


@router.post('/set_settings/{settings}')
async def send(settings) -> dict:

    return {"test": 123}



