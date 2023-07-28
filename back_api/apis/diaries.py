import warnings

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, UUID4

warnings.simplefilter(action='ignore', category=FutureWarning)

diaries_api = APIRouter(prefix='/diaries', tags=['diaries'])


class Diary(BaseModel):
    user_id: UUID4
    title: str
    content: str

# {
#     "user_id": "550e8400-e29b-41d4-a716-446655440000",
#     "title": "제목",
#     "content": "내용"
# }


# 다이어리 작성
@diaries_api.post("/")
async def create_diary(item: Diary):
    return HTTPException(status_code=501, detail="Not implemented (create_diary))")


# 전체 다이어리 조회
@diaries_api.get("/{user_id}")
async def get_diaries(user_id: UUID4):
    return HTTPException(status_code=501, detail="Not implemented (get_diaries)")


# 특정 다이어리 조회
@diaries_api.get("/{user_id}/{diary_id}")
async def get_diary(user_id: UUID4, diary_id: UUID4):
    return HTTPException(status_code=501, detail="Not implemented (get_diary)")


# 다이어리 수정
@diaries_api.put("/{user_id}/{diary_id}")
async def update_diary(user_id: UUID4, diary_id: UUID4, item: Diary):
    return HTTPException(status_code=501, detail="Not implemented (update_diary)")