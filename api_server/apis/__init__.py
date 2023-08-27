import os
import traceback
from datetime import datetime
from enum import Enum

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from pydantic import BaseModel
from pymongo import MongoClient


class MeloDB:
    def __init__(self):
        DB_ID = os.environ.get('DB_ID')
        DB_PASSWORD = os.environ.get('DB_PASSWORD')
        client = MongoClient(f'mongodb://{DB_ID}:{DB_PASSWORD}@mongo', 27017)
        self.melo_db = client['melovision']
        self.melo_users = self.melo_db['users']
        # self.melo_babies = self.melo_db['babies']
        # self.melo_diaries = self.melo_db['diaries']
        # self.melo_letters = self.melo_db['letters']
        # self.melo_chats = self.melo_db['chats']
        # self.melo_images = self.melo_db['images']
        self.melo_music = self.melo_db['music']
        self.melo_temp_music = self.melo_db['temp_music']


class ResponseModels:
    class UserIdResponse(BaseModel):
        user_id: str

    class BabyIdResponse(BaseModel):
        baby_id: str

    class MusicIdResponse(BaseModel):
        music_id: str

    class MusicInfoResponse(BaseModel):
        music_id: str
        genre: str
        instrument: str
        mood: str
        speed: str
        title: str
        desc: str
        generated_time: str


class Sex(str, Enum):
    male = 'male'
    female = 'female'


def object_id_to_str(documents):
    result = []
    for document in documents:
        document['_id'] = str(document['_id'])
        result.append(document)

    return result


def str_to_object_id(string):
    try:
        return ObjectId(string)
    except InvalidId:
        raise HTTPException(status_code=400, detail=f"Invalid ObjectId ({string})")
    # TODO: string 반환 안하게 바꾸기


def return_internal_server_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            print(traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"Internal Server Error ({e})")

    return wrapper
    # TODO: 추후 서비스 개시 전 삭제


def get_generated_time(object_id):
    timestamp = object_id.generation_time
    timestamp_datetime = datetime.fromtimestamp(timestamp.timestamp())
    return timestamp_datetime.strftime("%Y-%m-%d %H:%M:%S")
