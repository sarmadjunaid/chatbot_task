import openai
from config import OPENAI_SECRET_KEY


class OpenAIManager:

    def __init__(self):
        self.key = OPENAI_SECRET_KEY
