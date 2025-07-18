import time
import requests

TOKEN = '7933362286:AAHeMBOdZRpaOKeuQoOgASlOULaMTP9996c'
URL = f'https://api.telegram.org/bot{TOKEN}'

WELCOME_TEXT = (
    "📢 Gemini AI Pro with Veo 3 Now Available\n"
    "Includes 2TB Cloud Backup | 1-Year Access\n\n"
    "Proceed with the payment below to continue."
)

PAYMENT_TEXT = (
    "📌 *Payment Instructions*\n\n"
    "To complete your purchase:\n\n"
    "- Send ₹99 to UPI: `pay9570@airtel`\n"
    "- Then send a screenshot here: @PeruHACKER\n\n"
    "Our team will confirm and activate your subscription."
)

def send_message(chat_id, text, buttons=None):
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    if buttons:
        payload['reply_markup'] = {'inline_keyboard': buttons}
    requests.post(f'{URL}/sendMessage', json=payload)

def get_updates(offset=None):
    params = {'timeout': 30, 'offset': offset}
    res = requests.get(f'{URL}/getUpdates', params=params)
    return res.json()

def main():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates.get('result', []):
            offset = update['update_id'] + 1
            if 'message' in update and update['message']['text'] == '/start':
                chat_id = update['message']['chat']['id']
                send_message(chat_id, WELCOME_TEXT, [
                    [{'text': '💳 Get Gemini Pro Now', 'callback_data': 'pay_now'}]
                ])
            elif 'callback_query' in update and update['callback_query']['data'] == 'pay_now':
                chat_id = update['callback_query']['message']['chat']['id']
                send_message(chat_id, PAYMENT_TEXT)
        time.sleep(1)

if __name__ == '__main__':
    main()
