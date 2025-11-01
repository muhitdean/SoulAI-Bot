import os
import telebot
import requests

# Получаем переменные окружения
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# ⚠️ ДОБАВЬ ЭТУ ПРОВЕРКУ ⚠️
print(f"TELEGRAM_TOKEN: {'***' + TELEGRAM_TOKEN[-10:] if TELEGRAM_TOKEN else 'NOT SET!'}")
print(f"GROQ_API_KEY: {'***' + GROQ_API_KEY[-10:] if GROQ_API_KEY else 'NOT SET!'}")

if not TELEGRAM_TOKEN:
    print("❌ КРИТИЧЕСКАЯ ОШИБКА: TELEGRAM_TOKEN не установлен!")
    print("Добавь TELEGRAM_TOKEN в Environment Variables в Render!")
    exit(1)

if not GROQ_API_KEY:
    print("❌ КРИТИЧЕСКАЯ ОШИБКА: GROQ_API_KEY не установлен!")
    print("Добавь GROQ_API_KEY в Environment Variables в Render!")
    exit(1)

print("✅ Environment Variables загружены успешно!")
# 🔧 ФУНКЦИЯ ДЛЯ GROQ API
def ask_groq(message_text, prompt_type="psychologist"):
    """Функция для общения с Groq API"""
    try:
        print(f"🔍 Запрос к Groq: {message_text[:50]}...")
        
        # Выбираем промт по специализации
        prompts = {
            "psychologist": "Ты - SoulAI психолог. Говори эмпатично на казахском и русском. Помогай разбираться в эмоциях.",
            "coach": "Ты - SoulAI коуч. Помогай ставить цели и находить мотивацию. Будь энергичным.", 
            "hr": "Ты - SoulAI HR аналитик. Анализируй эмоциональное состояние и давай рекомендации."
        }
        
        system_prompt = prompts.get(prompt_type, "Ты - полезный помощник.")
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message_text}
            ],
            "model": "llama-3.1-8b-instant",
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        print(f"📡 Отправка запроса к Groq API...")
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        print(f"📊 Статус ответа: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Ошибка HTTP: {response.status_code}")
            return "Кешіріңіз, техникалық қате. 😔"
        
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        
        print(f"✅ Успешный ответ от Groq")
        return answer
        
    except Exception as e:
        print(f"❌ Ошибка Groq API: {e}")
        return "Кешіріңіз, техникалық қате. 😔"

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ОБРАБОТЧИКИ СООБЩЕНИЙ
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Сәлем! Я SoulAI - твой AI-помощник! Используй /psychologist, /coach или /hr")

@bot.message_handler(commands=['psychologist', 'coach', 'hr'])
def set_mode(message):
    mode = message.text[1:]  # Убираем слеш
    bot.reply_to(message, f"✅ Режим {mode} активирован! Теперь я в этом режиме.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    answer = ask_groq(message.text)
    bot.reply_to(message, answer)

# ЗАПУСК БОТА
print("🟢 SoulAI бот запущен!")
bot.polling(none_stop=True)
