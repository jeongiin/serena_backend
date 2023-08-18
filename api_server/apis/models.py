import io
import os
import warnings

import requests
from PIL import Image
from bson import ObjectId
from fastapi import HTTPException, APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
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
    instrument: str
    speed: Speed
    duration: Duration
    emotion: str
    title: str
    desc: str


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

    music_id = ObjectId()
    item = item.model_dump(mode='json')
    item['music_id'] = str(music_id)
    item['instrument'] = item['instrument'].replace(" ", "")

    response = requests.get('http://music_gen:45678/music', params=item)
    data_stream = io.BytesIO(response.content)

    if item['title'] == 'test' or True:
        return StreamingResponse(data_stream, media_type="audio/x-wav")
        # return FileResponse(os.path.join(music_outputs_path, '64d457149fa87d80fcb9af50.wav'))
    else:
        return FileResponse(os.path.join(music_outputs_path, f'{str(music_id)}.wav'))


# 생성 음악 저장하기
@models_api.post("/music/save")
async def save_generated_music(image_file: UploadFile,
                               user_id: str = Form(...),
                               music_id: str = Form(...),
                               genre: Genre = Form(...),
                               instrument: str = Form(...),
                               speed: Speed = Form(...),
                               duration: Duration = Form(...),
                               emotion: str = Form(...),
                               title: str = Form(...),
                               desc: str = Form(...)):
    item = dict({
        "_id": str_to_object_id(music_id),
        "user_id": user_id,
        "genre": genre,
        "instrument": instrument.replace(" ", "").split(","),
        "speed": speed,
        "duration": duration,
        "emotion": emotion,
        "title": title,
        "desc": desc,
    })

    music_id = MeloDB.melo_music.insert_one(item).inserted_id

    image_file_extension = image_file.filename.split('.')[-1].lower()
    if image_file_extension not in ['jpg', 'jpeg', 'png', 'heic']:
        raise HTTPException(status_code=400, detail="Invalid image file extension")

    try:
        image = Image.open(image_file.file)
        image = image.convert('RGB')
        image.save(os.path.join(music_thumbnails_path, f'{str(music_id)}.jpg'))

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Upload failed {e}")

    if title == 'test':
        return JSONResponse(status_code=200, content={"music_id": "64d457149fa87d80fcb9af50"})
    else:
        return JSONResponse(status_code=200, content={"music_id": str(music_id)})


# 생성 음악 정보 가져오기
@models_api.get("/music/info")
async def get_generated_music_info(user_id: str = None, music_id: str = None):
    if user_id:  # 특정 유저가 생성한 모든 음악 정보 가져오기
        user_id = str_to_object_id(user_id)
        user = MeloDB.melo_users.find_one({"_id": user_id}, {'_id': False})
        if not user:
            raise HTTPException(status_code=404, detail="User Not found")

        music = MeloDB.melo_music.find({"user_id": str(user_id)})
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

    # instrument 리스트를 string으로 변환
    music['instrument'] = ','.join(music['instrument'])

    return FileResponse(os.path.join(music_outputs_path, '64d457149fa87d80fcb9af50.wav'))
    # return FileResponse(os.path.join(music_outputs_path, f'{str(music_id)}.wav'))


# 생성 음악 썸네일 가져오기
@models_api.get("/music/thumbnail")
async def get_generated_music_thumbnail(music_id: str):
    music_id = str_to_object_id(music_id)
    music = MeloDB.melo_music.find_one({"_id": music_id}, {'_id': False})
    if not music:
        raise HTTPException(status_code=404, detail="Music Not found")

    # instrument 리스트를 string으로 변환
    music['instrument'] = ','.join(music['instrument'])

    return FileResponse(os.path.join(music_thumbnails_path, f'{str(music_id)}.jpg'))


# 생성 음악 제거
@models_api.delete("/music")
async def delete_generated_music(music_id: str):
    music_id = str_to_object_id(music_id)
    music = MeloDB.melo_music.find_one({"_id": music_id}, {'_id': False})
    if not music:
        raise HTTPException(status_code=404, detail="Not found")

    MeloDB.melo_music.delete_one({"_id": music_id})
    os.remove(os.path.join(music_outputs_path, f'{str(music_id)}.wav'))
    os.remove(os.path.join(music_thumbnails_path, f'{str(music_id)}.jpg'))

    return JSONResponse(status_code=200, content={"music_id": str(music_id)})


@models_api.get("/emotions")
async def get_emotions(desc: str):
    params = dict({
        "text": desc
    })

    response = requests.get('http://classify_emotions:56789/emotions', params=params)
    emotions = response.json()

    return JSONResponse(status_code=200, content=emotions)
