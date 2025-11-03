import os
import openai
from database import Database  # только этот импорт

class AIModule:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.db = Database()
    # ... остальной код ...
