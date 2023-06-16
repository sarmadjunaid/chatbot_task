from mongodb import MongoService
from loguru import logger


class ChatManager:

    def __init__(self):
        self._db = MongoService(db_name='chat_db', collection_name='messages')

    def save_message(self, data):
        try:
            self._db.add(data=data)
        except Exception as e:
            logger.error(f"Error during adding message; {e}")
