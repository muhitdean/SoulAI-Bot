import os
import requests

class Database:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
    
    def save_conversation(self, user_id, user_message, bot_response, emotion):
        return True
    
    def get_user_history(self, user_id, limit=5):
        return []
