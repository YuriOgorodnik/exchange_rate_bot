import json
import os
from datetime import datetime
import requests
import telebot

CURRENCY_RATES_FILE = "currency.json"
API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
YOUR_TOKEN_HERE = '6086053008:AAEwO6sILx8baNOlK6ljxLsIw_IOu96WwMc'
chat_id = "5352047072"
message = "Курс доллара изменился, срочно беги в банк!!!"


def main():
    """
    Основная функция программы.
    Получает и выводит на экран текущий курс USD к рублю от API.
    Записывает полученные данные в JSON-файл.
    """
    currency = "USD"
    rate = get_currency_rate(currency)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(f"Курс {currency} к рублю: {rate}")
    data = {"currency": currency, "rate": rate, "timestamp": timestamp}
    save_to_json(data)

    # если курс валюты отличается от предыдущего, то уведомляем об этом пользователя сообщением в Телеграмм-бот
    if rate != open_json()[-2]['rate']:
        bot = telebot.TeleBot(YOUR_TOKEN_HERE)
        bot.send_message(chat_id, message)


def get_currency_rate(base: str) -> float:
    """Получает курс валюты от API и возвращает его в виде float"""

    url = "https://api.apilayer.com/exchangerates_data/latest"
    response = requests.get(url, headers={'apikey': API_KEY}, params={'base': base})
    rate = response.json()['rates']['RUB']
    return rate


def save_to_json(data: dict) -> None:
    """Сохраняет данные в JSON-файл"""

    with open(CURRENCY_RATES_FILE, "a") as f:
        if os.stat(CURRENCY_RATES_FILE).st_size == 0:
            json.dump([data], f)
        else:
            with open(CURRENCY_RATES_FILE) as json_file:
                data_list = json.load(json_file)
            data_list.append(data)
            with open(CURRENCY_RATES_FILE, "w") as json_file:
                json.dump(data_list, json_file)


def open_json():
    with open(CURRENCY_RATES_FILE, "r", encoding='UTF-8') as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    main()
