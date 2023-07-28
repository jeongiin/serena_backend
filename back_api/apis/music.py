import warnings

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, UUID4

warnings.simplefilter(action='ignore', category=FutureWarning)

music_api = APIRouter(prefix='/music', tags=['music'])


# 생성 음악 가져오기
@music_api.get("/{user_id}/{music_id}")
async def get_generated_music(user_id: UUID4, music_id: UUID4):
    return HTTPException(status_code=501, detail="Not implemented (get_generated_music)")


# 생성 음악 제거
@music_api.delete("/{user_id}/{music_id}")
async def delete_generated_music(user_id: UUID4, music_id: UUID4):
    return HTTPException(status_code=501, detail="Not implemented (delete_generated_music)")
