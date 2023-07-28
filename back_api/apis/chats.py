import warnings
from pydantic import BaseModel
from uuid import UUID

from fastapi import HTTPException, APIRouter

warnings.simplefilter(action='ignore', category=FutureWarning)

chats_api = APIRouter(prefix='/chats', tags=['chats'])


class Chat(BaseModel):
    user_id: UUID
    title: str
    content: str


@chats_api.post("/")
async def create_diary():
    return HTTPException(status_code=501, detail="Not implemented")