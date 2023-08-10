import warnings
from enum import Enum

from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

from . import MeloDB, str_to_object_id

warnings.simplefilter(action='ignore', category=FutureWarning)

MeloDB = MeloDB()
models_api = APIRouter(prefix='/models', tags=['models'])


class Genre(str, Enum):
    classic = 'classic'
    jazz = 'jazz'
    pop = 'pop'
    rock = 'rock'
    hiphop = 'hiphop'


class Instrument(str, Enum):
    piano = 'piano'
    guitar = 'guitar'
    drum = 'drum'
    organ = 'organ'
    clarinet = 'clarinet'


class Speed(str, Enum):
    slow = 'slow'
    medium = 'medium'
    fast = 'fast'


class Duration(str, Enum):
    ten_seconds = '10s'
    thirty_seconds = '30s'
    one_minute = '1m'
    one_minute_thirty_seconds = '1m30s'
    two_minutes = '2m'


class ImageGenerateQuery(BaseModel):
    user_id: str
    baby_id: str
    # content_type: ContentType
    # content_id: str
    genre: Genre
    instrument: Instrument
    speed: Speed
    duration: Duration


class MusicGenerateQuery(BaseModel):
    user_id: str
    genre: Genre
    instrument: Instrument
    speed: Speed
    duration: Duration


class MusicSaveQuery(BaseModel):
    user_id: str
    music_id: str
    title: str
    desc: str = None


# 생성 앨범아트 이미지 생성하기
@models_api.post("/images")
async def create_generated_albumart_image(item: ImageGenerateQuery):
    # content_type_map = {
    #     ContentType.diary: MeloDB.melo_diaries,
    #     ContentType.letter: MeloDB.melo_letters,
    #     ContentType.chat: MeloDB.melo_chats,
    # }
    #
    # content_id = str_to_object_id(item.content_id)
    # content = content_type_map[item.content_type].find_one({"_id": content_id, "user_id": item.user_id, "baby_id": item.baby_id})
    # if not content:
    #     raise HTTPException(status_code=404, detail="Not found")

    # -------------------------------------------
    # # TODO: 모델에 이미지 생성 요청하는 코드 작성
    # -------------------------------------------

    # image_id = MeloDB.melo_images.insert_one(item.model_dump(mode='json')).inserted_id
    #
    # return JSONResponse(status_code=201, content={"image_id": str(image_id)})

    raise HTTPException(status_code=501, detail="Not implemented (create_generated_albumart_image)")


# 생성 앨범아트 이미지 가져오기
@models_api.get("/images")
async def get_generated_albumart_image(user_id: str, baby_id: str, image_id: str):
    image_id = str_to_object_id(image_id)
    image = MeloDB.melo_images.find_one({"_id": image_id, "user_id": user_id, "baby_id": baby_id})
    if not image:
        raise HTTPException(status_code=404, detail="Not found")

    image['_id'] = str(image['_id'])

    return JSONResponse(status_code=200, content=image['content'])


# 생성 앨범아트 이미지 제거
@models_api.delete("/images")
async def delete_generated_albumart_image(user_id: str, baby_id: str, image_id: str):
    image_id = str_to_object_id(image_id)
    image = MeloDB.melo_images.find_one({"_id": image_id, "user_id": user_id, "baby_id": baby_id})
    if not image:
        raise HTTPException(status_code=404, detail="Not found")

    MeloDB.melo_images.delete_one({"_id": image_id, "user_id": user_id, "baby_id": baby_id})

    return JSONResponse(status_code=200, content={"image_id": str(image_id)})


# 생성 음악 생성하기
@models_api.post("/music")
async def create_generated_music(item: MusicGenerateQuery):
    user_id = str_to_object_id(item.user_id)
    user = MeloDB.melo_users.find_one({"_id": user_id}, {'_id': False})
    if not user:
        raise HTTPException(status_code=404, detail="User Not found")

    # -------------------------------------------
    # # TODO: 모델에 음악 생성 요청하는 코드 작성
    # -------------------------------------------

    item = item.model_dump(mode='json')

    music_id = MeloDB.melo_music.insert_one(item.copy()).inserted_id
    item['music_id'] = str(music_id)

    return FileResponse('/api/music_outputs/test2.wav', filename='test2.wav', headers=item)
    # return FileResponse(f'/api/music_outputs/{item["music_id"]}.wav', filename=f'{item["music_id"]}.wav', headers=item)
    # return JSONResponse(status_code=200, content={"music_id": str(music_id)})


# 생성 음악 저장하기
@models_api.post("/music/save")
async def save_generated_music(item: MusicSaveQuery):
    user_id = str_to_object_id(item.user_id)
    music_id = str_to_object_id(item.music_id)
    user = MeloDB.melo_users.find_one({"_id": user_id}, {'_id': False})
    if not user:
        raise HTTPException(status_code=404, detail="User Not found")

    music_info = MeloDB.melo_music.find_one({"_id": music_id})

    item = item.model_dump(mode='json')
    item['genre'] = music_info.genre
    item['instrument'] = music_info.instrument
    item['speed'] = music_info.speed
    item['duration'] = music_info.duration
    del item['music_id']

    MeloDB.melo_music.update_one({"_id": music_id}, {"$set": item})

    return JSONResponse(status_code=200, content={"music_id": str(music_id)})


# 생성 음악 가져오기
@models_api.get("/music")
async def get_generated_music(user_id: str, music_id: str):
    user_id = str_to_object_id(user_id)
    music_id = str_to_object_id(music_id)
    user = MeloDB.melo_users.find_one({"_id": user_id}, {'_id': False})
    if not user:
        raise HTTPException(status_code=404, detail="User Not found")

    music = MeloDB.melo_music.find_one({"_id": music_id}, {'_id': False})
    if not music:
        raise HTTPException(status_code=404, detail="Music Not found")

    return FileResponse('/api/music_outputs/test1.wav', filename='test1.wav', headers=music)


# 생성 음악 제거
@models_api.delete("/music")
async def delete_generated_music(user_id: str, music_id: str):
    user_id = str_to_object_id(user_id)
    music_id = str_to_object_id(music_id)
    user = MeloDB.melo_users.find_one({"_id": user_id}, {'_id': False})
    if not user:
        raise HTTPException(status_code=404, detail="User Not found")

    music = MeloDB.melo_music.find_one({"_id": music_id}, {'_id': False})
    if not music:
        raise HTTPException(status_code=404, detail="Not found")

    MeloDB.melo_music.delete_one({"_id": music_id})

    return JSONResponse(status_code=200, content={"music_id": str(music_id)})
