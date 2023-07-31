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
