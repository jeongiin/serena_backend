import warnings
from enum import Enum

from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from . import MeloDB, str_to_object_id

warnings.simplefilter(action='ignore', category=FutureWarning)

MeloDB = MeloDB()
images_api = APIRouter(prefix='/images', tags=['images'])


class ContentType(str, Enum):
    diary = 'diary'
    letter = 'letter'
    chat = 'chat'


class AlbumArt(BaseModel):
    user_id: str
    baby_id: str
    content_type: ContentType
    content_id: str


# 생성 앨범아트 이미지 생성하기
@images_api.post("/albumart")
async def create_generated_albumart_image(item: AlbumArt):
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
    # # TODO: 모델에 이미지 생성 요청하는 코드 작성
    # -------------------------------------------

    # image_id = MeloDB.melo_images.insert_one(item.model_dump(mode='json')).inserted_id
    #
    # return JSONResponse(status_code=201, content={"image_id": str(image_id)})

    raise HTTPException(status_code=501, detail="Not implemented (create_generated_albumart_image)")


# 생성 앨범아트 이미지 가져오기
@images_api.get("/albumart")
async def get_generated_albumart_image(user_id: str, baby_id: str, image_id: str):
    image_id = str_to_object_id(image_id)
    image = MeloDB.melo_images.find_one({"_id": image_id, "user_id": user_id, "baby_id": baby_id})
    if not image:
        raise HTTPException(status_code=404, detail="Not found")

    image['_id'] = str(image['_id'])

    return JSONResponse(status_code=200, content=image['content'])
    # raise HTTPException(status_code=501, detail="Not implemented (get_generated_albumart_image)")


# 생성 앨범아트 이미지 제거
@images_api.delete("/albumart")
async def delete_generated_albumart_image(user_id: str, baby_id: str, image_id: str):
    image_id = str_to_object_id(image_id)
    image = MeloDB.melo_images.find_one({"_id": image_id, "user_id": user_id, "baby_id": baby_id})
    if not image:
        raise HTTPException(status_code=404, detail="Not found")

    MeloDB.melo_images.delete_one({"_id": image_id, "user_id": user_id, "baby_id": baby_id})

    return JSONResponse(status_code=200, content={"image_id": str(image_id)})
    # raise HTTPException(status_code=501, detail="Not implemented (delete_generated_albumart_image)")
