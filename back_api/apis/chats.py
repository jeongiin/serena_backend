import warnings

from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from . import MeloDB, object_id_to_str, str_to_object_id

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
    chat_id = MeloDB.melo_chats.insert_one(item.model_dump(mode='json')).inserted_id

    return JSONResponse(status_code=201, content={"chat_id": str(chat_id)})


# 전체, 개별 채팅 조회
@chats_api.get("/")
async def get_chats(user_id: str, baby_id: str, chat_id: str = None):
    if chat_id:
        chat_id = str_to_object_id(chat_id)
        chat = MeloDB.melo_chats.find_one({"_id": chat_id, "user_id": user_id, "baby_id": baby_id})
        if not chat:
            raise HTTPException(status_code=404, detail="Not found")

        chat['_id'] = str(chat['_id'])

        return JSONResponse(status_code=200, content=chat)
    else:
        chats = MeloDB.melo_chats.find({"user_id": user_id, "baby_id": baby_id})
        chats = object_id_to_str(chats)
        if not chats:
            raise HTTPException(status_code=404, detail="Not found")

        return JSONResponse(status_code=200, content=chats)


# 채팅 삭제
@chats_api.delete("/")
async def delete_chat(user_id: str, baby_id: str, chat_id: str):
    chat_id = str_to_object_id(chat_id)
    chat = MeloDB.melo_chats.find_one({"_id": chat_id, "user_id": user_id, "baby_id": baby_id})
    if not chat:
        raise HTTPException(status_code=404, detail="Not found")

    MeloDB.melo_chats.delete_one({"_id": chat_id, "user_id": user_id, "baby_id": baby_id})

    return JSONResponse(status_code=200, content={"chat_id": str(chat_id)})
