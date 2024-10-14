# models.py
from pymongo import MongoClient

class MongoDB:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["todo_db"]
        self.collection = self.db["tasks"]

mongo_db = MongoDB()

class Task:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
        }
