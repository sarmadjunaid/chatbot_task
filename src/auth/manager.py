from mongodb import MongoService


class AuthManager:

    def __init__(self):
        self.db = MongoService(db_name='chat_db', collection_name='users')

    def handle_user_data(self, userinfo, token):

        data = {
            "meta": {},
            "token": token,
            **userinfo
        }
        self.db.add(data)