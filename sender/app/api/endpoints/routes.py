from sender.app.memory.relational.postgresql import Redirects
from fastapi import APIRouter
from typing import Union, List

router = APIRouter()

DEFAULT_SERVER_ERROR_CASE_RESPONSE = {"code": 500}


async def create_redirect(copy_from: Union[int, str], copy_to: Union[int, str]) -> Redirects:
    from loader import sender
    copy_from_name = await sender.get_chat_name(copy_from)
    copy_to_name = await sender.get_chat_name(copy_to)
    redirect = Redirects(
        copy_from=str(copy_from),
        copy_to=str(copy_to),
        copy_to_name=copy_to_name,
        copy_from_name=copy_from_name
    )
    return redirect


@router.post('/add_redirect/{copy_from}_{copy_to}')
async def add_redirect(copy_from: Union[int, str], copy_to: Union[int, str]) -> dict:
    from loader import postgres_manager
    redirect = await create_redirect(copy_from, copy_to)

    if await postgres_manager.add_redirect(redirect):
        return {
            "code": 200,
            "info": f"RedirectObject ([{copy_from}] --> [{copy_to}]) created and added to database"
        }

    else:
        return DEFAULT_SERVER_ERROR_CASE_RESPONSE


@router.post('/remove_redirect/{redirect_id}')
async def remove_redirect(redirect_id: int) -> dict:
    from loader import postgres_manager
    if await postgres_manager.remove_redirect(redirect_id):
        return {
            "code": 200,
            "info": f"Removed RedirectObject at ({redirect_id}) id"
        }

    else:
        return DEFAULT_SERVER_ERROR_CASE_RESPONSE


@router.post('/update_redirect/{redirect_id}_{copy_from}_{copy_to}')
async def update_redirect(redirect_id: int, copy_from: Union[int, str], copy_to: Union[int, str]) -> dict:
    from loader import postgres_manager
    redirect = await create_redirect(copy_from, copy_to)

    if await postgres_manager.update_redirect(redirect_id, redirect):
        return {
            "code": 200,
            "info": f"updated RedirectObject at ({redirect_id}) id with values(coppy_from={copy_from}, copy_to={copy_to})"
        }

    else:
        return DEFAULT_SERVER_ERROR_CASE_RESPONSE


@router.post('/get_all_redirects')
async def get_all_redirects() -> dict:
    from loader import postgres_manager
    redirects: List[Redirects] = await postgres_manager.get_all_redirects()
    if redirects:
        return {
            "code": 200,
            "info": [redirect[0].__dict__ for redirect in redirects]
        }

    else:
        return DEFAULT_SERVER_ERROR_CASE_RESPONSE


@router.post('/remove_all_redirects')
async def remove_all_redirects() -> dict:
    from loader import postgres_manager
    if await postgres_manager.remove_all_redirects():
        return {
            "code": 200,
            "info": "all redirects were successfully deleted"
        }

    else:
        return DEFAULT_SERVER_ERROR_CASE_RESPONSE


@router.post('/copy_history/{copy_from}_{copy_to}')
async def copy_history(copy_from: Union[int, str], copy_to: Union[str, int]) -> dict:
    from loader import sender, message_transformer

    messages = await sender.copy(copy_from, limit=1000)
    messages_to_send = await message_transformer.transform_to_current_model(messages)
    if await sender.paste(copy_to, messages_to_send):
        return {
            "code": 200,
            "info": "success"
        }

    else:
        return DEFAULT_SERVER_ERROR_CASE_RESPONSE

