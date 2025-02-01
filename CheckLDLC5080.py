import requests
from bs4 import BeautifulSoup
import time

# Configurazione
URL = "https://www.ldlc.com/it-it/scheda/PB00660823.html"  # Modifica con il link del prodotto
TELEGRAM_BOT_TOKEN = "8027736178:AAG05kRXGJnlgKjeiIz7tg2hhYk2-n3-sLA"
TELEGRAM_CHAT_ID = "328887957"

def check_availability():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    # LDLC usa la classe "stocks" per la disponibilità
    availability = soup.find("div", class_="stocks").get_text(strip=True)

    if "En stock" in availability:  # Controlla se il prodotto è disponibile
        message = f"🎉 Il prodotto è DISPONIBILE! Acquistalo ora: {URL}"
        send_telegram_notification(message)
    else:
        print("Ancora non disponibile...")

def send_telegram_notification(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(telegram_url, json=payload)

# Esegue il controllo ogni 10 minuti
while True:
    check_availability()
    time.sleep(600)  # Attendi 10 minuti prima di ricontrollare
