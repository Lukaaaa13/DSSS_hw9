import telebot
import requests
import json
from telebot import types

TOKEN = token
API_ENDPOINT = 'http://127.0.0.1:1234/v1/chat/completions'

bot = telebot.TeleBot(TOKEN)

# Start command handler
# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Dear stranger! Want to grab a cup of tea?")


# Handle all other messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_input = message.text

    # Prepare the data for the API request
    api_data = {
        "messages": [
            {"role": "system",
             "content": "You are a formal assistant. Respond to the user's questions in a polite and professional manner."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.1,
        "max_tokens": 200,
        "stream": False
    }

    try:
        response = requests.post(API_ENDPOINT, json=api_data, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            api_response = response.json()
            assistant_response = api_response.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, no response from the AI.")
            bot.reply_to(message, assistant_response)

        else:
            bot.reply_to(message, "Sorry, something went wrong with the API request. Please try again later.")

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")


if __name__ == "__main__":
    bot.polling(none_stop=True)
