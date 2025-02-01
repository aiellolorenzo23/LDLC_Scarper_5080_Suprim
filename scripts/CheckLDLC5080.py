import requests
from bs4 import BeautifulSoup
import os

# Prende il Token e Chat ID dalle variabili d'ambiente di GitHub Actions
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Lista di URL dei prodotti su LDLC
PRODUCT_URLS = [
    "https://www.ldlc.com/it-it/scheda/PB00660823.html",  # Primo prodotto - MSI RTX 5080 SUPRIM SOC
    "https://www.ldlc.com/it-it/scheda/PB00660873.html"  # Secondo prodotto - MSI RTX 5080 VANGUARD SOC
]


def check_availability():
    headers = {"User-Agent": "Mozilla/5.0"}

    for url in PRODUCT_URLS:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        # LDLC usa la classe "stocks" per indicare la disponibilità
        availability = soup.find("div", class_="stocks").get_text(strip=True)

        if "En stock" in availability:
            send_telegram_notification(f"🎉 DISPONIBILE: {url}")
        else:
            print(f"Ancora non disponibile: {url}")


def send_telegram_notification(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)


# Esegui il controllo
check_availability()
