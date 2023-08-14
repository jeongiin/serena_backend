import os
import warnings
from PIL import Image

from fastapi import HTTPException, APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

from . import MeloDB, str_to_object_id, object_id_to_str, Genre, Instrument, Speed, Duration

warnings.simplefilter(action='ignore', category=FutureWarning)

MeloDB = MeloDB()
models_api = APIRouter(prefix='/models', tags=['models'])

music_outputs_path = os.path.join('/api', 'music_outputs')
music_thumbnails_path = os.path.join('/api', 'music_thumbnails')

os.makedirs(music_outputs_path, exist_ok=True)
os.makedirs(music_thumbnails_path, exist_ok=True)


class ImageGenerateQuery(BaseModel):
    user_id: str
    baby_id: str
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

    return FileResponse(os.path.join(music_outputs_path, '64d457149fa87d80fcb9af50.wav'), headers=item)
    # return FileResponse(os.path.join(music_outputs_path, f'{str(music_id)}.wav'), headers=item)


# 생성 음악 저장하기
@models_api.post("/music/save")
async def save_generated_music(image_file: UploadFile, music_id: str = Form(...), title: str = Form(...), desc: str = Form(...)):
    music_id = str_to_object_id(music_id)
    music_info = MeloDB.melo_music.find_one({"_id": music_id})
    if not music_info:
        raise HTTPException(status_code=404, detail="Music Not found")

    image_file_extension = image_file.filename.split('.')[-1].lower()
    if image_file_extension not in ['jpg', 'jpeg', 'png', 'heic']:
        raise HTTPException(status_code=400, detail="Invalid image file extension")

    try:
        image = Image.open(image_file.file)
        image = image.convert('RGB')
        image.save(os.path.join(music_thumbnails_path, f'{str(music_id)}.jpg'))

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Upload failed")

    item = dict({
        "user_id": music_info['user_id'],
        "title": title,
        "desc": desc,
        "genre": music_info['genre'],
        "instrument": music_info['instrument'],
        "speed": music_info['speed'],
        "duration": music_info['duration'],
    })

    MeloDB.melo_music.update_one({"_id": music_id}, {"$set": item})

    return JSONResponse(status_code=200, content={"music_id": str(music_id)})


# 생성 음악 정보 가져오기
@models_api.get("/music/info")
async def get_generated_music_info(user_id: str = None, music_id: str = None):
    if user_id:  # 특정 유저가 생성한 모든 음악 정보 가져오기
        user_id = str_to_object_id(user_id)
        user = MeloDB.melo_users.find_one({"_id": user_id}, {'_id': False})
        if not user:
            raise HTTPException(status_code=404, detail="User Not found")

        music = MeloDB.melo_music.find({"user_id": user_id})
        music = object_id_to_str(music)
        for i in range(len(music)):
            music[i]['music_id'] = music[i].pop('_id')

        return JSONResponse(status_code=200, content=music)

    elif music_id:  # 특정 음악 정보 가져오기
        music_id = str_to_object_id(music_id)
        music = MeloDB.melo_music.find_one({"_id": music_id}, {'_id': False})
        if not music:
            raise HTTPException(status_code=404, detail="Music Not found")

        return JSONResponse(status_code=200, content=music)

    else:  # 모든 음악 정보 가져오기
        music = MeloDB.melo_music.find({})
        music = object_id_to_str(music)
        for i in range(len(music)):
            music[i]['music_id'] = music[i].pop('_id')

        return JSONResponse(status_code=200, content=music)


# 생성 음악 파일 가져오기
@models_api.get("/music")
async def get_generated_music(music_id: str):
    music_id = str_to_object_id(music_id)
    music = MeloDB.melo_music.find_one({"_id": music_id}, {'_id': False})
    if not music:
        raise HTTPException(status_code=404, detail="Music Not found")

    # 헤더에 한글 전송 불가
    if 'title' in music.keys():
        del music['title'], music['desc']

    return FileResponse(os.path.join(music_outputs_path, '64d457149fa87d80fcb9af50.wav'), headers=music)
    # return FileResponse(os.path.join(music_outputs_path, f'{str(music_id)}.wav'), headers=music)


# 생성 음악 제거
@models_api.delete("/music")
async def delete_generated_music(music_id: str):
    music_id = str_to_object_id(music_id)
    music = MeloDB.melo_music.find_one({"_id": music_id}, {'_id': False})
    if not music:
        raise HTTPException(status_code=404, detail="Not found")

    MeloDB.melo_music.delete_one({"_id": music_id})
    os.remove(os.path.join(music_outputs_path, f'{str(music_id)}.wav'))

    return JSONResponse(status_code=200, content={"music_id": str(music_id)})
