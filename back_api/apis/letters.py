import warnings

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, UUID4

warnings.simplefilter(action='ignore', category=FutureWarning)

letters_api = APIRouter(prefix='/letters', tags=['letters'])


class Letter(BaseModel):
    user_id: UUID4
    title: str
    content: str


# {
#     "user_id": "550e8400-e29b-41d4-a716-446655440000",
#     "title": "제목",
#     "content": "내용"
# }


# 편지 작성
@letters_api.post("/")
async def create_letter(item: Letter):
    return HTTPException(status_code=501, detail="Not implemented (create_letter)")


# 전체 편지 조회
@letters_api.get("/{user_id}")
async def get_letters(user_id: UUID4):
    return HTTPException(status_code=501, detail="Not implemented (get_letters)")


# 특정 편지 조회
@letters_api.get("/{user_id}/{letter_id}")
async def get_letter(user_id: UUID4, letter_id: UUID4):
    return HTTPException(status_code=501, detail="Not implemented (get_letter)")


# 편지 수정
@letters_api.put("/{user_id}/{letter_id}")
async def update_letter(user_id: UUID4, letter_id: UUID4, item: Letter):
    return HTTPException(status_code=501, detail="Not implemented (update_letter)")


# 편지 삭제
@letters_api.delete("/{user_id}/{letter_id}")
async def delete_letter(user_id: UUID4, letter_id: UUID4):
    return HTTPException(status_code=501, detail="Not implemented (delete_letter)")
