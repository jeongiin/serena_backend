import warnings

from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from . import MeloDB, object_id_to_str, str_to_object_id

warnings.simplefilter(action='ignore', category=FutureWarning)

MeloDB = MeloDB()
letters_api = APIRouter(prefix='/letters', tags=['letters'])


class Letter(BaseModel):
    user_id: str
    baby_id: str
    title: str
    content: str


# 편지 작성
@letters_api.post("/")
async def create_letter(item: Letter):
    user = MeloDB.melo_users.find_one({"_id": str_to_object_id(item.user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Not found")

    letter_id = MeloDB.melo_letters.insert_one(item.model_dump(mode='json')).inserted_id

    return JSONResponse(status_code=201, content={"letter_id": str(letter_id)})


# 전체, 개별 편지 조회
@letters_api.get("/")
async def get_letters(user_id: str, baby_id: str, letter_id: str = None):
    if letter_id:
        letter_id = str_to_object_id(letter_id)
        letter = MeloDB.melo_letters.find_one({"_id": letter_id, "user_id": user_id, "baby_id": baby_id})
        if not letter:
            raise HTTPException(status_code=404, detail="Not found")

        letter['_id'] = str(letter['_id'])

        return JSONResponse(status_code=200, content=letter)
    else:
        letters = MeloDB.melo_letters.find({"user_id": user_id, "baby_id": baby_id})
        letters = object_id_to_str(letters)
        if not letters:
            raise HTTPException(status_code=404, detail="Not found")

        return JSONResponse(status_code=200, content=letters)


# 편지 수정
@letters_api.put("/")
async def update_letter(letter_id: str, item: Letter):
    letter_id = str_to_object_id(letter_id)
    letter = MeloDB.melo_letters.find_one({"_id": letter_id, "user_id": item.user_id, "baby_id": item.baby_id})
    if not letter:
        raise HTTPException(status_code=404, detail="Not found")

    MeloDB.melo_letters.update_one({"_id": letter_id, "user_id": item.user_id, "baby_id": item.baby_id}, {"$set": item.model_dump(mode='json')})

    return JSONResponse(status_code=200, content={"letter_id": str(letter_id)})


# 편지 삭제
@letters_api.delete("/")
async def delete_letter(user_id: str, baby_id: str, letter_id: str):
    letter_id = str_to_object_id(letter_id)
    letter = MeloDB.melo_letters.find_one({"_id": letter_id, "user_id": user_id, "baby_id": baby_id})
    if not letter:
        raise HTTPException(status_code=404, detail="Not found")

    MeloDB.melo_letters.delete_one({"_id": letter_id, "user_id": user_id, "baby_id": baby_id})

    return JSONResponse(status_code=200, content={"letter_id": str(letter_id)})
