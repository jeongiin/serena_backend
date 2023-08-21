import warnings

from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from . import MeloDB, object_id_to_str, str_to_object_id, return_internal_server_error, Sex

warnings.simplefilter(action='ignore', category=FutureWarning)

MeloDB = MeloDB()
common_api = APIRouter(prefix='/common', tags=['common'])


class User(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    desc: str = None
    expected_pd: int = None


class Baby(BaseModel):
    user_id: str
    name: str
    sex: Sex
    birth: str
    weeks: int
    desc: str = None


# 새 회원 정보 작성
@common_api.post("/users")
async def create_user(item: User):
    @return_internal_server_error
    def logic(variables):
        user_id = MeloDB.melo_users.insert_one(variables['item'].model_dump()).inserted_id

        return JSONResponse(status_code=201, content={"user_id": str(user_id)})

    return logic(locals())


# 회원 정보 조회
@common_api.get("/users")
async def get_user(user_id: str):
    @return_internal_server_error
    def logic(variables):
        user_id = str_to_object_id(variables['user_id'])
        user = MeloDB.melo_users.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="Not found")

        user['_id'] = str(user['_id'])

        return JSONResponse(status_code=200, content=user)

    return logic(locals())


# 회원 정보 수정
@common_api.put("/users")
async def update_user(user_id: str, item: User):
    @return_internal_server_error
    def logic(variables):
        user_id = str_to_object_id(variables['user_id'])
        user = MeloDB.melo_users.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="Not found")

        MeloDB.melo_users.update_one({"_id": user_id}, {"$set": variables['item'].model_dump()})

        return JSONResponse(status_code=200, content={"user_id": str(user_id)})

    return logic(locals())


# 회원 정보 삭제
@common_api.delete("/users")
async def delete_user(user_id: str):
    @return_internal_server_error
    def logic(variables):
        user_id = str_to_object_id(variables['user_id'])
        user = MeloDB.melo_users.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="Not found")

        MeloDB.melo_users.delete_one({"_id": user_id})

        return JSONResponse(status_code=200, content={"user_id": str(user_id)})

    return logic(locals())


# 새 아기 정보 작성
@common_api.post("/babies")
async def create_baby(item: Baby):
    @return_internal_server_error
    def logic(variables):
        user_id = str_to_object_id(variables['item'].user_id)
        user = MeloDB.melo_users.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="Not found")

        baby = variables['item'].model_dump()
        baby['user_id'] = str(user_id)
        baby_id = MeloDB.melo_babies.insert_one(baby).inserted_id

        return JSONResponse(status_code=201, content={"baby_id": str(baby_id)})

    return logic(locals())


# 전체, 개별 아기 정보 조회
@common_api.get("/babies")
async def get_babies(user_id: str, baby_id: str = None):
    @return_internal_server_error
    def logic(variables):
        if variables['baby_id']:
            baby_id = str_to_object_id(variables['baby_id'])
            baby = MeloDB.melo_babies.find_one({"_id": baby_id, "user_id": user_id})
            if not baby:
                raise HTTPException(status_code=404, detail="Not found")

            baby['_id'] = str(baby['_id'])

            return JSONResponse(status_code=200, content=baby)
        else:
            babies = MeloDB.melo_babies.find({"user_id": user_id})
            babies = object_id_to_str(babies)

            return JSONResponse(status_code=200, content=babies)

    return logic(locals())


# 아기 정보 수정
@common_api.put("/babies")
async def update_baby(baby_id: str, item: Baby):
    @return_internal_server_error
    def logic(variables):
        user_id = variables['item'].user_id
        baby_id = str_to_object_id(variables['baby_id'])
        baby = MeloDB.melo_babies.find_one({"_id": baby_id, "user_id": user_id})
        if not baby:
            raise HTTPException(status_code=404, detail="Not found")

        MeloDB.melo_babies.update_one({"_id": baby_id}, {"$set": variables['item'].model_dump()})

        return JSONResponse(status_code=200, content={"baby_id": str(baby_id)})

    return logic(locals())


# 아기 정보 삭제
@common_api.delete("/babies")
async def delete_baby(user_id: str, baby_id: str):
    @return_internal_server_error
    def logic(variables):
        user_id = variables['user_id']
        baby_id = str_to_object_id(variables['baby_id'])
        baby = MeloDB.melo_babies.find_one({"_id": baby_id, "user_id": user_id})
        if not baby:
            raise HTTPException(status_code=404, detail="Not found")

        MeloDB.melo_babies.delete_one({"_id": baby_id, "user_id": user_id})

        return JSONResponse(status_code=200, content={"baby_id": str(baby_id)})

    return logic(locals())
