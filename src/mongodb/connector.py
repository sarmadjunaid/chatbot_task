from pymongo import MongoClient
from datetime import datetime
from loguru import logger


class MongoService:

    def __init__(self, db_name: str, collection_name: str):
        self.mongo = MongoClient("mongodb://localhost:27017")
        self.db = self.mongo[db_name][collection_name]
        self._created_at = int(datetime.utcnow().timestamp())
        self._updated_at = int(datetime.utcnow().timestamp())

    def add(self, data: dict):
        try:
            data['meta']['created_at'] = self._created_at
            data['meta']['updated_at'] = self._updated_at

            self.db.insert_one(data)
            return True
        except Exception as e:
            logger.error(f"MongoDB: Error inserting data {e}")
            return False

    def update(self, data: dict, query: dict, many: bool = False):
        try:
            data['$set']['meta.updated_at'] = self._updated_at

            if many:
                self.db.update_many(filter=query, update=data)
            else:
                self.db.update_one(filter=query, update=data)

            return True
        except Exception as e:
            logger.error(f"MongoDB: Error updating data {e}")
            return False

    def get(self, query: dict = None, _all: bool = False):
        try:
            if _all and query:
                return self.db.find(query)
            elif _all:
                return self.db.find()
            else:
                return self.db.find_one(query)

        except Exception as e:
            logger.error(f"MongoDB: Error fetching data {e}")
            return False

    def delete(self, query: dict, many: bool = False):
        try:
            if many:
                self.db.delete_many(filter=query)
            else:
                self.db.delete_one(filter=query)

            return True
        except Exception as e:
            logger.error(f"MongoDB: Error deleting data {e}")
            return False