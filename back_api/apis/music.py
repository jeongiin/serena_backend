import warnings
from enum import Enum

from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from . import MeloDB, str_to_object_id, object_id_to_str

warnings.simplefilter(action='ignore', category=FutureWarning)

MeloDB = MeloDB()
music_api = APIRouter(prefix='/music', tags=['music'])


class ContentType(str, Enum):
    diary = 'diary'
    letter = 'letter'
    chat = 'chat'


class Music(BaseModel):
    user_id: str
    baby_id: str
    content_type: ContentType
    content_id: str


# 생성 음악 생성하기
@music_api.post("/")
async def create_generated_music(item: Music):
    content_type_map = {
        ContentType.diary: MeloDB.melo_diaries,
        ContentType.letter: MeloDB.melo_letters,
        ContentType.chat: MeloDB.melo_chats,
    }

    content_id = str_to_object_id(item.content_id)
    content = content_type_map[item.content_type].find_one({"_id": content_id, "user_id": item.user_id, "baby_id": item.baby_id})
    if not content:
        raise HTTPException(status_code=404, detail="Not found")

    # -------------------------------------------
    # # TODO: 모델에 음악 생성 요청하는 코드 작성
    # -------------------------------------------

    # music_id = MeloDB.melo_musics.insert_one(item.model_dump(mode='json')).inserted_id
    #
    # return JSONResponse(status_code=201, content={"music_id": str(music_id)})

    raise HTTPException(status_code=501, detail="Not implemented (create_generated_music)")

# 생성 음악 가져오기
@music_api.get("/{user_id}/{music_id}")
async def get_generated_music(user_id: str, baby_id: str, music_id: str):
    music_id = str_to_object_id(music_id)
    music = MeloDB.melo_music.find_one({"_id": music_id, "user_id": user_id, "baby_id": baby_id})
    if not music:
        raise HTTPException(status_code=404, detail="Not found")

    music['id'] = object_id_to_str(music['_id'])

    return JSONResponse(status_code=200, content=music['content'])
    # raise HTTPException(status_code=501, detail="Not implemented (get_generated_music)")


# 생성 음악 제거
@music_api.delete("/{user_id}/{music_id}")
async def delete_generated_music(user_id: str, baby_id: str, music_id: str):
    music_id = str_to_object_id(music_id)
    music = MeloDB.melo_music.find_one({"_id": music_id, "user_id": user_id, "baby_id": baby_id})
    if not music:
        raise HTTPException(status_code=404, detail="Not found")

    MeloDB.melo_music.delete_one({"_id": music_id, "user_id": user_id, "baby_id": baby_id})

    return JSONResponse(status_code=200, content={"music_id": str(music_id)})
    # raise HTTPException(status_code=501, detail="Not implemented (delete_generated_music)")
