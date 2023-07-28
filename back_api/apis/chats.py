import warnings
from uuid import UUID

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

warnings.simplefilter(action='ignore', category=FutureWarning)

chats_api = APIRouter(prefix='/chats', tags=['chats'])


class Chat(BaseModel):
    user_id: UUID
    title: str
    content: str


# 채팅 작성
@chats_api.post("/")
async def create_diary(item: Chat):
    return HTTPException(status_code=501, detail="Not implemented")


# 전체 채팅 조회
@chats_api.get("/")
async def get_diaries(user_id: UUID):
    return HTTPException(status_code=501, detail="Not implemented")


# 특정 채팅 조회
@chats_api.get("/{chat_id}")
async def get_diary(chat_id: UUID):
    return HTTPException(status_code=501, detail="Not implemented")