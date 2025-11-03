import os
import openai
from database import Database

class AIModule:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.db = Database()
    
    def generate_response(self, user_id, user_message):
        try:
            # Упрощенная версия без анализа эмоций сначала
            history = self.db.get_user_history(user_id)
            
            prompt = self.build_prompt(user_message, history)
            response = self.get_ai_response(prompt)
            
            # Сохраняем с базовой эмоцией
            self.db.save_conversation(user_id, user_message, response, "neutral")
            
            return response
        except Exception as e:
            return "Привет! Я SoulAI. Расскажи, что у тебя на душе? 💫"
    
    def build_prompt(self, message, history):
        history_text = ""
        for chat in reversed(history):
            history_text += f"User: {chat['user_message']}\nBot: {chat['bot_response']}\n\n"
        
        return f"""
Ты SoulAI - эмпатичный психологический помощник.

История диалога:
{history_text if history_text else 'Первый диалог'}

Сообщение пользователя: "{message}"

Ответь с эмпатией и поддержкой, как добрый друг.
"""
    
    def get_ai_response(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content
        except:
            return "Я здесь чтобы поддержать тебя! Расскажи, что происходит? 💭"
