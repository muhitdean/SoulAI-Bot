import os
import openai

class AIModule:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def generate_response(self, user_id, user_message):
        try:
            prompt = f"""
Ты SoulAI - эмпатичный психологический помощник.

Сообщение пользователя: "{user_message}"

Ответь с эмпатией и поддержкой, как добрый друг.
Будь теплым, понимающим и помогающим.
"""
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return "Я здесь чтобы поддержать тебя! Расскажи, что происходит? 💭"
