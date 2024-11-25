from .models import *
import requests

TELEGRAM_BOT_TOKEN = '7537240849:AAFs2eNrst2_n90t3iDW2G8d3s7n1Yz6F3g'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

def send_telegram_message(chat_id, message):
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(TELEGRAM_API_URL, data=payload)
    if response.status_code != 200:
        print(f'Failed to send message to {chat_id}')
    else:
        print(f'Message sent to {chat_id}')

def notify_clients():
    today = timezone.now().date()
    three_days_after = today + timezone.timedelta(days=3)
    staff = User.objects.filter(is_superuser=True).last()

    # Filter clients with payment_date equal to today
    clients_today = Client.objects.filter(payment_date=today)
    for client in clients_today:
        send_telegram_message(client.user.last_name, f'Тариф закончился!\n\nКлиент: {client.name}\nТелефон: {client.phone}\nДата платежа: {client.payment_date}')
        send_telegram_message(staff.last_name, f'Тариф закончился!\n\nКлиент: {client.name}\nТелефон: {client.phone}\nДата платежа: {client.payment_date}')

    # Filter clients with payment_date before three days ago
    clients_three_days_after = Client.objects.filter(payment_date=three_days_after)
    for client in clients_three_days_after:
        send_telegram_message(client.user.last_name, f'До оплаты осталось 3 дня!\n\nКлиент: {client.name}\nТелефон: {client.phone}\nДата платежа: {client.payment_date}')
        send_telegram_message(staff.last_name, f'До оплаты осталось 3 дня!\n\nКлиент: {client.name}\nТелефон: {client.phone}\nДата платежа: {client.payment_date}')

if __name__ == '__main__':
    notify_clients()