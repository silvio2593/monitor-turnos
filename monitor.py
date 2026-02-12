import json
import os
import requests
from bs4 import BeautifulSoup

URL = "https://www.cgbahiablanca.com.ar/tramites/citas/pasaportes1/solicitar-cita-pasaporte-espanol.html"
NO_CITAS_PHRASE = "En este momento no hay citas disponibles"
STATE_FILE = "state.json"

BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TG_CHAT_ID", "")

def send_telegram(msg: str):
    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(api, json={"chat_id": CHAT_ID, "text": msg})

def fetch_text() -> str:
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    return " ".join(soup.get_text(separator=" ").split())

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def main():
    text = fetch_text()
    has_no_citas = NO_CITAS_PHRASE in text

    state = load_state()
