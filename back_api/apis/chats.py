import warnings

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

from . import MeloDB

warnings.simplefilter(action='ignore', category=FutureWarning)

MeloDB = MeloDB()
chats_api = APIRouter(prefix='/chats', tags=['chats'])


class Chat(BaseModel):
    user_id: str
    baby_id: str
    title: str
    content: str



# 채팅 작성
@chats_api.post("/")
async def create_chat(item: Chat):
    raise HTTPException(status_code=501, detail="Not implemented (create_chat)")


# 전체 채팅 조회
@chats_api.get("/")
async def get_chats(user_id: str):
    raise HTTPException(status_code=501, detail="Not implemented (get_chats)")


# 특정 채팅 조회
@chats_api.get("/")
async def get_chat(user_id: str, chat_id: str):
    raise HTTPException(status_code=501, detail="Not implemented (get_chat)")


# 채팅 삭제
@chats_api.delete("/")
async def delete_chat(user_id: str, chat_id: str):
    raise HTTPException(status_code=501, detail="Not implemented (delete_chat)")


if __name__ == '__main__':
    pass
