from sender.app.memory.relational.postgresql import Redirects
from sender.app.utils.data_validator import InputValidator
from typing import Union, List, Dict, Final
from fastapi import APIRouter

router = APIRouter()
input_validator = InputValidator()

DEFAULT_ERROR_RESPONSE: Final[Dict] = {"code": 500, "info": False}
DEFAULT_SUCCESS_RESPONSE: Final[Dict] = {"code": 200, "info": True}


async def create_redirect(copy_from: Dict, copy_to: Dict) -> Redirects:
    copy_to_id = copy_to["chat_id"]
    copy_from_id = copy_from["chat_id"]
    copy_to_name = copy_to["chat_name"]
    copy_from_name = copy_from["chat_name"]

    redirect = Redirects(
        copy_from=copy_from_id,
        copy_to=copy_to_id,
        copy_to_name=copy_to_name,
        copy_from_name=copy_from_name
    )

    return redirect


@router.post('/add_redirect/{copy_from}_{copy_to}')
async def add_redirect(copy_from: Union[int, str], copy_to: Union[int, str]) -> Dict:
    from loader import postgres_manager

    copy_from = await input_validator.try_parse(copy_from)
    copy_to = await input_validator.try_parse(copy_to)
    redirect = await create_redirect(copy_from, copy_to)

    if await postgres_manager.add_redirect(redirect):
        return DEFAULT_SUCCESS_RESPONSE
    else:
        return DEFAULT_ERROR_RESPONSE


@router.post('/remove_redirect/{redirect_id}')
async def remove_redirect(redirect_id: int) -> Dict:
    from loader import postgres_manager

    if await postgres_manager.remove_redirect(redirect_id):
        return DEFAULT_SUCCESS_RESPONSE
    else:
        return DEFAULT_ERROR_RESPONSE


@router.post('/update_redirect/{redirect_id}_{copy_from}_{copy_to}')
async def update_redirect(redirect_id: int, copy_from: Union[int, str], copy_to: Union[int, str]) -> Dict:
    from loader import postgres_manager

    copy_from = await input_validator.try_parse(copy_from)
    copy_to = await input_validator.try_parse(copy_to)
    redirect = await create_redirect(copy_from, copy_to)

    if await postgres_manager.update_redirect(redirect_id, redirect):
        return DEFAULT_SUCCESS_RESPONSE
    else:
        return DEFAULT_ERROR_RESPONSE


@router.post('/get_all_redirects')
async def get_all_redirects() -> Dict:
    from loader import postgres_manager
    redirects: List[Redirects] = await postgres_manager.get_all_redirects()

    if redirects:
        response = DEFAULT_SUCCESS_RESPONSE.copy()
        response["info"] = [redirect[0].__dict__ for redirect in redirects]
        return response

    else:
        return DEFAULT_ERROR_RESPONSE


@router.post('/remove_all_redirects')
async def remove_all_redirects() -> Dict:
    from loader import postgres_manager

    if await postgres_manager.remove_all_redirects():
        return DEFAULT_SUCCESS_RESPONSE

    else:
        return DEFAULT_ERROR_RESPONSE


@router.post('/copy_history/{copy_from}_{copy_to}')
async def copy_history(copy_from: Union[int, str], copy_to: Union[str, int]) -> Dict:
    from loader import sender, message_transformer

    copy_from = await input_validator.try_parse(copy_from)
    copy_to = await input_validator.try_parse(copy_to)

    messages = await sender.copy(copy_from["chat_id"], limit=1000)
    messages_to_send = await message_transformer.transform_to_current_model(messages)
    if await sender.paste(copy_to["chat_id"], messages_to_send):
        return DEFAULT_SUCCESS_RESPONSE

    else:
        return DEFAULT_ERROR_RESPONSE


@router.post('/validate/{chat_hint}')
async def validate_chat_id(chat_hint: Union[str, int]) -> Dict:

    if await input_validator.validate_chat(chat_hint):
        return DEFAULT_SUCCESS_RESPONSE

    else:
        return DEFAULT_ERROR_RESPONSE

