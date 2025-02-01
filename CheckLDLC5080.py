import requests
from bs4 import BeautifulSoup
import os

# Prende il Token e Chat ID dalle variabili d'ambiente di GitHub Actions
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# URL del prodotto su LDLC
PRODUCT_URL = "https://www.ldlc.com/fiche/PB00483577.html"

def check_availability():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(PRODUCT_URL, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    # LDLC usa la classe "stocks" per indicare la disponibilità
    availability = soup.find("div", class_="stocks").get_text(strip=True)

    if "En stock" in availability:
        send_telegram_notification(f"🎉 DISPONIBILE: {PRODUCT_URL}")
    else:
        print("Ancora non disponibile...")

def send_telegram_notification(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)

# Esegui il controllo
check_availability()
