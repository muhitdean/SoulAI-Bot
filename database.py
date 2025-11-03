import os

class Database:
    def __init__(self):
        pass
    
    def save_conversation(self, user_id, user_message, bot_response, emotion):
        """Временно не сохраняем в базу"""
        return True
    
    def get_user_history(self, user_id, limit=5):
        """Временно не используем историю"""
        return []
