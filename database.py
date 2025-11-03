import os
import requests

class Database:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
    
    def save_conversation(self, user_id, user_message, bot_response, emotion):
        # ... остальной код БЕЗ supabase ...
