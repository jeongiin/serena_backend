import warnings
from uuid import UUID

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

warnings.simplefilter(action='ignore', category=FutureWarning)

letters_api = APIRouter(prefix='/letters', tags=['letters'])


class Letter(BaseModel):
    user_id: UUID
    title: str
    content: str


# 편지 작성
@letters_api.post("/")
async def create_diary(item: Letter):
    return HTTPException(status_code=501, detail="Not implemented")


# 전체 편지 조회
@letters_api.get("/")
async def get_diaries(user_id: UUID):
    return HTTPException(status_code=501, detail="Not implemented")


# 특정 편지 조회
@letters_api.get("/{letter_id}")
async def get_diary(letter_id: UUID):
    return HTTPException(status_code=501, detail="Not implemented")
