import warnings

from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from . import MeloDB, object_id_to_str, str_to_object_id

warnings.simplefilter(action='ignore', category=FutureWarning)

MeloDB = MeloDB()
diaries_api = APIRouter(prefix='/diaries', tags=['diaries'])


class Diary(BaseModel):
    user_id: str
    baby_id: str
    title: str
    content: str


# 다이어리 작성
@diaries_api.post("/")
async def create_diary(item: Diary):
    diary_id = MeloDB.melo_diaries.insert_one(item.model_dump(mode='json')).inserted_id

    return JSONResponse(status_code=201, content={"diary_id": str(diary_id)})


# 전체 다이어리 조회
@diaries_api.get("/{user_id}")
async def get_diaries(user_id: str, baby_id: str):
    diaries = MeloDB.melo_diaries.find({"user_id": user_id, "baby_id": baby_id})
    diaries = object_id_to_str(diaries)
    if not diaries:
        raise HTTPException(status_code=404, detail="Not found")

    return JSONResponse(status_code=200, content=diaries)


# 특정 다이어리 조회
@diaries_api.get("/{user_id}/{diary_id}")
async def get_diary(user_id: str, diary_id: str, baby_id: str):
    diary_id = str_to_object_id(diary_id)
    diary = MeloDB.melo_diaries.find_one({"_id": diary_id, "user_id": user_id, "baby_id": baby_id})
    if not diary:
        raise HTTPException(status_code=404, detail="Not found")

    diary['_id'] = str(diary['_id'])

    return JSONResponse(status_code=200, content=diary)


# 다이어리 수정
@diaries_api.put("/{user_id}/{diary_id}")
async def update_diary(user_id: str, diary_id: str, item: Diary):
    diary_id = str_to_object_id(diary_id)
    diary = MeloDB.melo_diaries.find_one({"_id": diary_id, "user_id": user_id, "baby_id": item.baby_id})
    if not diary:
        raise HTTPException(status_code=404, detail="Not found")

    MeloDB.melo_diaries.update_one({"_id": diary_id, "user_id": user_id, "baby_id": item.baby_id}, {"$set": item.model_dump(mode='json')})

    return JSONResponse(status_code=200, content={"diary_id": str(diary_id)})


# 다이어리 삭제
@diaries_api.delete("/{user_id}/{diary_id}")
async def delete_diary(user_id: str, diary_id: str, baby_id: str):
    diary_id = str_to_object_id(diary_id)
    diary = MeloDB.melo_diaries.find_one({"_id": diary_id, "user_id": user_id, "baby_id": baby_id})
    if not diary:
        raise HTTPException(status_code=404, detail="Not found")

    MeloDB.melo_diaries.delete_one({"_id": diary_id, "user_id": user_id, "baby_id": baby_id})

    return JSONResponse(status_code=200, content={"diary_id": str(diary_id)})
