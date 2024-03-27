import os
import requests

from dotenv import load_dotenv

load_dotenv()


def send_message(message):
    token = os.environ.get('TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    params = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print(f'Error sending message: {response.status_code} {response.text}')
    else:
        print('Message sent successfully!')
