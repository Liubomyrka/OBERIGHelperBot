import requests

TOKEN = "7730295760:AAGuRYKPmnwhJospsWS4dbHW0yy3M6JrZRk"

try:
    response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe")
    if response.status_code == 200:
        print("✅ Токен коректний. Ось дані про вашого бота:")
        print(response.json())
    else:
        print("❌ Помилка: Токен некоректний або недійсний.")
        print(f"HTTP Status Code: {response.status_code}")
        print(response.json())
except Exception as e:
    print("❌ Виникла помилка під час виконання запиту:")
    print(e)
