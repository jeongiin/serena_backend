import io
import os
import warnings

import requests
from PIL import Image
from bson import ObjectId
from fastapi import HTTPException, APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from pydantic import BaseModel

from . import MeloDB, ResponseModels, str_to_object_id, object_id_to_str, return_internal_server_error, get_generated_time

warnings.simplefilter(action='ignore', category=FutureWarning)

MeloDB = MeloDB()
models_api = APIRouter(prefix='/models', tags=['models'])

music_outputs_path = os.path.join('/api', 'music_outputs')
music_thumbnails_path = os.path.join('/api', 'music_thumbnails')

os.makedirs(music_outputs_path, exist_ok=True)
os.makedirs(music_thumbnails_path, exist_ok=True)


class MusicGenerateQuery(BaseModel):
    user_id: str
    title: str = None
    desc: str = None


class MusicSaveQuery(BaseModel):
    user_id: str
    music_id: str
    title: str = None
    desc: str = None


# 생성 음악 생성하기
@models_api.post("/music", deprecated=True, response_class=StreamingResponse, responses={200: {"content": {"audio/x-wav": {}},
                                                                                               "headers": {"prompt": {},
                                                                                                           "music_id": {},
                                                                                                           "generated_time": {}}}})
async def create_generated_music(item: MusicGenerateQuery):
    """
    # 음악 생성하기

    ## Request Body
    - user_id: 유저 id, string
    - title: 제목, string, default: None
    - desc: 설명, string

    ## Response Headers
    - prompt: 생성된 음악의 prompt, string
    - music_id: 생성된 음악의 id, string
    - generated_time: 생성된 음악의 생성 시간, string

    ## Response Body
    - 생성된 음악 파일, audio/x-wav

    """

    @return_internal_server_error
    async def logic(variables):
        user_id = str_to_object_id(variables['item'].user_id)
        user = MeloDB.melo_users.find_one({"_id": user_id}, {'_id': False})
        if not user:
            raise HTTPException(status_code=404, detail="User Not found")

        music_id = ObjectId()
        item = variables['item'].model_dump(mode='json')
        item['music_id'] = str(music_id)

        response = requests.get('http://music_gen:44444/music', params=item)
        if response.status_code == 500:
            raise HTTPException(status_code=500, detail="Out of Memory")

        prompt = response.headers['prompt']
        data_stream = io.BytesIO(response.content)
        with open(os.path.join(music_outputs_path, f'{str(music_id)}.wav'), 'wb') as f:
            f.write(data_stream.getbuffer())

        generated_time = get_generated_time(music_id)

        response_headers = {
            "prompt": prompt,
            "music_id": str(music_id),
            "generated_time": generated_time,
        }

        if item['title'] == 'test' or True:
            return StreamingResponse(data_stream, media_type="audio/x-wav", headers=response_headers)
        else:
            return FileResponse(os.path.join(music_outputs_path, f'{str(music_id)}.wav'))

    return await logic(locals())


# 음악 생성하기 Ver 2
@models_api.post("/music/v2", response_class=StreamingResponse)
async def create_generated_music_v2(image: UploadFile, user_id: str = Form(...), emotion: str = Form(...)):
    """
    # 음악 생성하기 Ver 2

    ## Request Body
    - image: 썸네일 이미지 파일, image/jpg, image/jpeg, image/png, image/heic
    - user_id: 유저 id, string
    - emotion: 현재 감정, string

    ## Response Headers
    - caption: 생성된 음악의 caption, string
    - prompt: 생성된 음악의 prompt, string
    - genre: 생성된 음악의 장르, string
    - instrument: 생성된 음악의 악기, string, comma separated, ex) piano, guitar, drum
    - mood: 생성된 음악의 무드, string
    - speed: 생성된 음악의 속도, string
    - music_id: 생성된 음악의 id, string
    - generated_time: 생성된 음악의 생성 시간, string

    ## Response Body
    - 생성된 음악 파일, audio/x-wav
    """

    @return_internal_server_error
    async def logic(variables):
        image = variables['image']
        user_id = str_to_object_id(variables['user_id'])
        user = MeloDB.melo_users.find_one({"_id": user_id}, {'_id': False})
        if not user:
            raise HTTPException(status_code=404, detail="User Not found")

        music_id = ObjectId()
        generated_time = get_generated_time(music_id)
        genre = user['genre']
        emotion = variables['emotion']

        image_extension = image.filename.split('.')[-1].lower()
        if image_extension not in ['jpg', 'jpeg', 'png', 'heic']:
            raise HTTPException(status_code=415, detail="Unsupported Media Type (Invalid image file extension)")

        response = requests.post('http://image_to_text:55555/caption', files={'image': image.file})
        caption = response.json()['caption']

        response = requests.get('http://music_gen:44444/music', params={'caption': caption, 'genre': genre, 'emotion': emotion})
        if response.status_code == 500:
            raise HTTPException(status_code=500, detail=response.content.decode("utf-8"))

        data_stream = io.BytesIO(response.content)
        with open(os.path.join(music_outputs_path, f'{str(music_id)}.wav'), 'wb') as f:
            f.write(data_stream.getbuffer())

        image = Image.open(image.file)
        image = image.convert('RGB')
        image.save(os.path.join(music_thumbnails_path, f'{str(music_id)}.jpg'))

        db_data = {
            "_id": music_id,
            "user_id": str(user_id),
            "caption": caption,
            "prompt": response.headers['prompt'],
            "genre": response.headers['genre'],
            "instrument": response.headers['instrument'],
            "mood": response.headers['mood'],
            "speed": response.headers['speed'],
            "title": None,
            "desc": None,
            "generated_time": generated_time,
        }
        music_id = MeloDB.melo_temp_music.insert_one(db_data).inserted_id

        response_headers = {
            "music_id": str(music_id),
            "caption": caption,
            "prompt": response.headers['prompt'],
            "genre": response.headers['genre'],
            "instrument": response.headers['instrument'],
            "mood": response.headers['mood'],
            "speed": response.headers['speed'],
            "generated_time": generated_time,
        }

        return StreamingResponse(data_stream, media_type="audio/x-wav", headers=response_headers)

    return await logic(locals())


# 생성 음악 저장하기
@models_api.post("/music/save", response_model=ResponseModels.MusicIdResponse, deprecated=True)
async def save_generated_music(image: UploadFile,
                               user_id: str = Form(...),
                               music_id: str = Form(...),
                               title: str = Form(...),
                               desc: str = Form(...)):
    """
    # 음악 저장하기

    ## Request Body
    - image: 썸네일 이미지 파일, image/jpg, image/jpeg, image/png, image/heic
    - user_id: 유저 id, string
    - music_id: 음악 id, string
    - title: 제목, string
    - desc: 설명, string

    ## Response
    - music_id: 저장된 음악의 id, string
    """

    @return_internal_server_error
    async def logic(variables):
        item = dict({
            "_id": str_to_object_id(variables['music_id']),
            "user_id": variables['user_id'],
            "genre": variables['genre'],
            "title": variables['title'],
            "desc": variables['desc'],
            "generated_time": get_generated_time(str_to_object_id(variables['music_id'])),
        })

        music = MeloDB.melo_music.find_one({"_id": item['_id']}, {'_id': False})
        if music:
            raise HTTPException(status_code=409, detail="Music already exists")

        music_id = MeloDB.melo_music.insert_one(item).inserted_id

        image_extension = image.filename.split('.')[-1].lower()
        if image_extension not in ['jpg', 'jpeg', 'png', 'heic']:
            raise HTTPException(status_code=415, detail="Unsupported Media Type (Invalid image file extension)")

        try:
            image = Image.open(image.file)
            image = image.convert('RGB')
            image.save(os.path.join(music_thumbnails_path, f'{str(music_id)}.jpg'))

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=f"Upload failed {e}")

        if title == 'test':
            return JSONResponse(status_code=200, content={"music_id": "64d457149fa87d80fcb9af50"})
        else:
            return JSONResponse(status_code=200, content={"music_id": str(music_id)})

    return await logic(locals())


# 생성 음악 저장하기 Ver 2
@models_api.post("/music/save/v2", response_model=ResponseModels.MusicIdResponse)
async def save_generated_music_v2(item: MusicSaveQuery):
    @return_internal_server_error
    async def logic(variables):
        music_id = str_to_object_id(variables['item'].music_id)
        music = MeloDB.melo_temp_music.find_one({"_id": music_id}, {'_id': False})
        if not music:
            raise HTTPException(status_code=404, detail="Music Not found")

        item = variables['item'].model_dump(mode='json')
        item['_id'] = music_id
        item['caption'] = music['caption']
        item['prompt'] = music['prompt']
        item['genre'] = music['genre']
        item['instrument'] = music['instrument']
        item['mood'] = music['mood']
        item['speed'] = music['speed']
        item['generated_time'] = music['generated_time']
        del item['music_id']
        music_id = MeloDB.melo_music.insert_one(item).inserted_id
        MeloDB.melo_temp_music.delete_one({"_id": music_id})

        return JSONResponse(status_code=200, content={"music_id": str(music_id)})

    return await logic(locals())


# 생성 음악 정보 가져오기
@models_api.get("/music/info", response_model=ResponseModels.MusicInfoResponse)
async def get_generated_music_info(user_id: str = None, music_id: str = None):
    """
    # 음악 정보 가져오기

    ## Request Body
    - user_id: 유저 id, string, default: None
    - music_id: 음악 id, string, default: None

    ## Response
    - music_id: 음악 id, string
    - genre: 장르, string
    - instrument: 악기, string, comma separated, ex) piano, guitar, drum
    - mood: 무드, string
    - speed: 속도, string
    - title: 제목, string
    - desc: 설명, string
    - generated_time: 생성 시간, string

    ### user_id가 주어진 경우
    - 해당 유저가 생성한 모든 음악 정보

    ### music_id가 주어진 경우
    - 해당 음악 정보

    ### 아무것도 주어지지 않은 경우
    - 모든 음악 정보
    """

    @return_internal_server_error
    async def logic(variables):
        if variables['user_id']:  # 특정 유저가 생성한 모든 음악 정보 가져오기
            user_id = str_to_object_id(variables['user_id'])
            user = MeloDB.melo_users.find_one({"_id": user_id}, {'_id': False})
            if not user:
                raise HTTPException(status_code=404, detail="User Not found")

            music = MeloDB.melo_music.find({"user_id": str(user_id)})
            music = object_id_to_str(music)
            for i in range(len(music)):
                music[i]['music_id'] = music[i].pop('_id')

            return JSONResponse(status_code=200, content=music)

        elif variables['music_id'] or (variables['user_id'] and variables['music_id']):  # 특정 음악 정보 가져오기
            music_id = str_to_object_id(variables['music_id'])
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

    return await logic(locals())


# 생성 음악 파일 가져오기
@models_api.get("/music", response_class=FileResponse, responses={200: {"content": {"audio/x-wav": {}}}})
async def get_generated_music(music_id: str):
    """
    # 음악 파일 가져오기

    ## Parameters
    - music_id: 음악 id, string

    ## Response
    - 생성된 음악 파일: audio/x-wav
    """

    @return_internal_server_error
    async def logic(variables):
        music_id = str_to_object_id(variables['music_id'])
        music = MeloDB.melo_music.find_one({"_id": music_id}, {'_id': False})
        if not music:
            raise HTTPException(status_code=404, detail="Music Not found")

        return FileResponse(os.path.join(music_outputs_path, f'{str(music_id)}.wav'))

    return await logic(locals())


# 생성 음악 썸네일 가져오기
@models_api.get("/music/thumbnail", response_class=FileResponse, responses={200: {"content": {"image/jpg": {}}}})
async def get_generated_music_thumbnail(music_id: str):
    """
    # 음악 썸네일 가져오기

    ## Parameters
    - music_id: 음악 id, string

    ## Response
    - 생성된 음악 썸네일 파일: image/jpg
    """

    @return_internal_server_error
    async def logic(variables):
        music_id = str_to_object_id(variables['music_id'])
        music = MeloDB.melo_music.find_one({"_id": music_id}, {'_id': False})
        if not music:
            raise HTTPException(status_code=404, detail="Music Not found")

        return FileResponse(os.path.join(music_thumbnails_path, f'{str(music_id)}.jpg'))

    return await logic(locals())


# 생성 음악 제거
@models_api.delete("/music", response_model=ResponseModels.MusicIdResponse)
async def delete_generated_music(music_id: str):
    """
    # 음악 제거

    ## Parameters
    - music_id: 음악 id, string

    ## Response
    - music_id: 제거된 음악의 id, string
    """

    @return_internal_server_error
    async def logic(variables):
        music_id = str_to_object_id(variables['music_id'])
        music = MeloDB.melo_music.find_one({"_id": music_id}, {'_id': False})
        if not music:
            raise HTTPException(status_code=404, detail="Music Not found")

        MeloDB.melo_music.delete_one({"_id": music_id})
        os.remove(os.path.join(music_outputs_path, f'{str(music_id)}.wav'))
        os.remove(os.path.join(music_thumbnails_path, f'{str(music_id)}.jpg'))

        return JSONResponse(status_code=200, content={"music_id": str(music_id)})

    return await logic(locals())
