from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from pymongo import MongoClient


class MeloDB:
    def __init__(self):
        client = MongoClient('mongodb://root:root@localhost', 27017)
        self.melo_db = client['melovision']
        self.melo_users = self.melo_db['users']
        self.melo_babies = self.melo_db['babies']
        self.melo_diaries = self.melo_db['diaries']
        self.melo_letters = self.melo_db['letters']
        self.melo_chats = self.melo_db['chats']
        self.melo_images = self.melo_db['images']
        self.melo_music = self.melo_db['music']


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
