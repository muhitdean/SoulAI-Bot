import os
import telebot
import requests
import logging
from prompts import PSYCHOLOGIST_PROMPT, COACH_PROMPT, HR_ANALYST_PROMPT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Храним контекст для каждого пользователя
user_sessions = {}

def ask_groq(message_text, user_id, prompt_type="psychologist"):
    """Умный AI с выбором специализации"""
    
    # Выбираем промт по специализации
    prompts = {
        "psychologist": PSYCHOLOGIST_PROMPT,
        "coach": COACH_PROMPT, 
        "hr": HR_ANALYST_PROMPT
    }
    
    system_prompt = prompts.get(prompt_type, PSYCHOLOGIST_PROMPT)
    
    # Добавляем историю диалога (последние 5 сообщений)
    if user_id not in user_sessions:
        user_sessions[user_id] = []
    
    user_sessions[user_id].append({"role": "user", "content": message_text})
    
    # Ограничиваем историю 5 последними сообщениями
    if len(user_sessions[user_id]) > 5:
        user_sessions[user_id] = user_sessions[user_id][-5:]
    
    # Формируем полный контекст
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(user_sessions[user_id])
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "messages": messages,
                "model": "llama-3.3-70b-versatile",
                "temperature": 0.8,
                "max_tokens": 500
            },
            timeout=10
        )
        
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        
        # Сохраняем ответ в историю
        user_sessions[user_id].append({"role": "assistant", "content": answer})
        
        return answer
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        return "Кешіріңіз, техникалық қате. 😔"

@bot.message_handler(commands=['start'])
def start(message):
    text = """
👋 Сәлем! Я SoulAI - твой умный помощник!

Выбери режим:
/psychologist - Психолог (эмоции, стресс)
/coach - Коуч (цели, мотивация)  
/hr - HR аналитик (анализ состояния)

Просто напиши - и я помогу! 🧠
    """
    bot.reply_to(message, text)

@bot.message_handler(commands=['psychologist', 'coach', 'hr'])
def set_mode(message):
    user_id = message.from_user.id
    mode = message.text[1:]  # Убираем слеш
    
    # Сохраняем выбранный режим
    if user_id not in user_sessions:
        user_sessions[user_id] = []
    
    user_sessions[user_id].append({"mode": mode})
    
    modes = {
        "psychologist": "🧠 Режим психолога",
        "coach": "🎯 Режим коуча", 
        "hr": "📊 HR аналитик"
    }
    
    bot.reply_to(message, f"✅ {modes[mode]} активирован!")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    prompt_type = "psychologist"  # По умолчанию
    
    # Определяем тип промта по истории или командам
    if user_id in user_sessions:
        for msg in user_sessions[user_id]:
            if msg.get("mode"):
                prompt_type = msg["mode"]
                break
    
    answer = ask_groq(message.text, user_id, prompt_type)
    bot.reply_to(message, answer)

if __name__ == "__main__":
    logger.info("🚀 Умный SoulAI запущен!")
    bot.infinity_polling()
