import os
from supabase import create_client

class Database:
    def __init__(self):
        self.client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        self.setup_tables()
    
    def setup_tables(self):
        """Создаем таблицы если их нет"""
        try:
            # Таблица пользователей
            self.client.table("users").insert({
                "user_id": "setup",
                "created_at": "2024-01-01"
            }).execute()
        except:
            pass  # Таблица уже существует
    
    def save_conversation(self, user_id, user_message, bot_response, emotion):
        """Сохраняем диалог в базу"""
        data = {
            "user_id": user_id,
            "user_message": user_message,
            "bot_response": bot_response,
            "emotion_detected": emotion
        }
        return self.client.table("conversations").insert(data).execute()
    
    def get_user_history(self, user_id, limit=5):
        """Получаем историю диалогов пользователя"""
        try:
            response = self.client.table("conversations")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            return response.data
        except:
            return []
