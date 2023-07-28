import warnings

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, UUID4

warnings.simplefilter(action='ignore', category=FutureWarning)

chats_api = APIRouter(prefix='/chats', tags=['chats'])


class Chat(BaseModel):
    user_id: UUID4
    title: str
    content: str


# 채팅 작성
@chats_api.post("/")
async def create_diary(item: Chat):
    return HTTPException(status_code=501, detail="Not implemented (create_diary))")


# 전체 채팅 조회
@chats_api.get("/{user_id}")
async def get_diaries(user_id: UUID4):
    return HTTPException(status_code=501, detail="Not implemented (get_diaries)")


# 특정 채팅 조회
@chats_api.get("/{user_id}/{chat_id}")
async def get_diary(user_id: UUID4, chat_id: UUID4):
    return HTTPException(status_code=501, detail="Not implemented (get_diary)")


# 채팅 수정
@chats_api.put("/{user_id}/{chat_id}")
async def update_diary(user_id: UUID4, chat_id: UUID4, item: Chat):
    return HTTPException(status_code=501, detail="Not implemented (update_diary)")