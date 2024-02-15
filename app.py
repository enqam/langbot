from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace these with your actual values
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    chat_id = update['message']['chat']['id']
    text = update['message']['text']

    # Call the function that generates a response from OpenAI's GPT
    gpt_response = generate_gpt_response(text)

    # Send the GPT-generated response back to the user via Telegram
    send_telegram_message(chat_id, gpt_response)

    return jsonify(success=True)

def generate_gpt_response(prompt):
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'text-davinci-003',  # Or whichever model you're using
        'prompt': prompt,
        'max_tokens': 150
    }
    response = requests.post('https://api.openai.com/v4/completions', headers=headers, json=data)
    result = response.json()
    return result['choices'][0]['text'].strip()

def send_telegram_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run()
