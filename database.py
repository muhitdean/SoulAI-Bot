import os
import requests
import json

class Database:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.setup_tables()
    
    def setup_tables(self):
        """Создаем таблицы через SQL"""
        try:
            # SQL для создания таблиц
            sql = """
            CREATE TABLE IF NOT EXISTS conversations (
                id SERIAL PRIMARY KEY,
                user_id TEXT,
                user_message TEXT,
                bot_response TEXT,
                emotion_detected TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
            """
            self.execute_sql(sql)
        except:
            pass  # Таблицы уже существуют
    
    def execute_sql(self, sql):
        """Выполняет SQL запрос через REST API"""
        url = f"{self.supabase_url}/rest/v1/"
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(url + "rpc/exec_sql", headers=headers, json={"query": sql})
        return response.json()
    
    def save_conversation(self, user_id, user_message, bot_response, emotion):
        """Сохраняем диалог в базу"""
        url = f"{self.supabase_url}/rest/v1/conversations"
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        data = {
            "user_id": user_id,
            "user_message": user_message,
            "bot_response": bot_response,
            "emotion_detected": emotion
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            return response.status_code == 201
        except:
            return False
    
    def get_user_history(self, user_id, limit=5):
        """Получаем историю диалогов пользователя"""
        url = f"{self.supabase_url}/rest/v1/conversations"
        params = {
            "user_id": f"eq.{user_id}",
            "order": "created_at.desc",
            "limit": limit
        }
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []
