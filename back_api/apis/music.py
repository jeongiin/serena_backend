import warnings

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

from . import MeloDB

warnings.simplefilter(action='ignore', category=FutureWarning)

MeloDB = MeloDB()
music_api = APIRouter(prefix='/music', tags=['music'])


class Music(BaseModel):
    user_id: str
    baby_id: str
    title: str
    content: str


# 생성 음악 생성하기
@music_api.post("/")
async def create_generated_music():
    raise HTTPException(status_code=501, detail="Not implemented (create_generated_music)")


# 생성 음악 가져오기
@music_api.get("/{user_id}/{music_id}")
async def get_generated_music(user_id: str, music_id: str):
    raise HTTPException(status_code=501, detail="Not implemented (get_generated_music)")


# 생성 음악 제거
@music_api.delete("/{user_id}/{music_id}")
async def delete_generated_music(user_id: str, music_id: str):
    raise HTTPException(status_code=501, detail="Not implemented (delete_generated_music)")
