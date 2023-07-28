import warnings

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, UUID4

warnings.simplefilter(action='ignore', category=FutureWarning)

common_api = APIRouter(prefix='/common', tags=['common'])


class User(BaseModel):
    name: str
    email: str = None
    phone: str = None
    address: str = None
    description: str = None


class Baby(BaseModel):
    name: str
    birth: str


# 새 회원 정보 작성
@common_api.post("/users")
async def create_user(item: User):
    return HTTPException(status_code=501, detail="Not implemented (create_user)")


# 회원 정보 조회
@common_api.get("/users/{user_id}")
async def get_user(user_id: UUID4):
    return HTTPException(status_code=501, detail="Not implemented (get_user)")


# 회원 정보 수정
@common_api.put("/users/{user_id}")
async def update_user(user_id: UUID4, item: User):
    return HTTPException(status_code=501, detail="Not implemented (update_user)")


# 회원 정보 삭제
@common_api.delete("/users/{user_id}")
async def delete_user(user_id: UUID4):
    return HTTPException(status_code=501, detail="Not implemented (delete_user)")


# 새 아기 정보 작성
@common_api.post("/babies/{user_id}")
async def create_baby(user_id: UUID4, item: Baby):
    return HTTPException(status_code=501, detail="Not implemented (create_baby)")


# 아기 정보 조회
@common_api.get("/babies/{user_id}")
async def get_babies(user_id: UUID4, baby_id: UUID4):
    return HTTPException(status_code=501, detail="Not implemented (get_babies)")


# 아기 정보 수정
@common_api.put("/babies/{user_id}/{baby_id}")
async def update_baby(user_id: UUID4, baby_id: UUID4, item: Baby):
    return HTTPException(status_code=501, detail="Not implemented (update_baby)")


# 아기 정보 삭제
@common_api.delete("/babies/{user_id}/{baby_id}")
async def delete_baby(user_id: UUID4, baby_id: UUID4):
    return HTTPException(status_code=501, detail="Not implemented (delete_baby)")