import time
import requests

TOKEN = '7933362286:AAHeMBOdZRpaOKeuQoOgASlOULaMTP9996c'
URL = f'https://api.telegram.org/bot{TOKEN}'

WELCOME_TEXT = (
    "🧠 *Gemini AI Pro with Veo 3*\n\n"
    "Includes 2TB Cloud Backup | 1-Year Access.\n\n"
    "Choose an option below:"
)

PAYMENT_TEXT = (
    "📌 *Payment Instructions*\n\n"
    "Send ₹99 to UPI ID: `pay9570@airtel`\n"
    "Then send a screenshot to: @PeruHACKER\n\n"
    "We'll confirm and activate your subscription."
)

GIVEAWAY_TEXT = (
    "🎉 *Join Giveaway!*\n\n"
    "Click the button below to enter.\n"
    "We'll randomly pick 3 winners by *12 PM tomorrow*.\n"
    "Good luck!"
)

CRYPTO_TEXT = (
    "💸 *Pay by Crypto*\n\n"
    "Contact here: @PeruHACKER to make payment using crypto (USDT, BTC, etc.)"
)

def send_message(chat_id, text, buttons=None):
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown',
    }
    if buttons:
        payload['reply_markup'] = {'inline_keyboard': buttons}
    requests.post(f'{URL}/sendMessage', json=payload)

def get_updates(offset=None):
    params = {'timeout': 30, 'offset': offset}
    res = requests.get(f'{URL}/getUpdates', params=params)
    return res.json()

def notify_admin(user):
    user_info = f"🎁 New Giveaway Entry\n\n👤 Name: {user.get('first_name', 'N/A')}\n🆔 ID: {user['id']}\n"
    requests.post(f'{URL}/sendMessage', json={
        'chat_id': '@PeruHACKER',
        'text': user_info
    })

def main():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates.get('result', []):
            offset = update['update_id'] + 1

            if 'message' in update and update['message'].get('text') == '/start':
                chat_id = update['message']['chat']['id']
                send_message(chat_id, WELCOME_TEXT, [
                    [{'text': '💳 Get Gemini Pro Now', 'callback_data': 'pay_now'}],
                    [{'text': '🎁 Join Giveaway', 'callback_data': 'join_giveaway'}]
                ])

            elif 'callback_query' in update:
                data = update['callback_query']['data']
                chat_id = update['callback_query']['message']['chat']['id']
                user = update['callback_query']['from']

                if data == 'pay_now':
                    send_message(chat_id, PAYMENT_TEXT, [
                        [{'text': '💰 Pay by Crypto', 'callback_data': 'crypto_pay'}]
                    ])
                elif data == 'crypto_pay':
                    send_message(chat_id, CRYPTO_TEXT)
                elif data == 'join_giveaway':
                    send_message(chat_id, GIVEAWAY_TEXT, [
                        [{'text': '✅ Enter Giveaway', 'callback_data': 'enter_giveaway'}]
                    ])
                elif data == 'enter_giveaway':
                    send_message(chat_id, "🎉 You’ve successfully entered the giveaway!")
                    notify_admin(user)

        time.sleep(1)

if __name__ == '__main__':
    main()
