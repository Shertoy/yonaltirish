# -*- coding: utf-8 -*-
"""
BIR MARTALIK skript: Telegram'ga "bu yerga yaz" deb aytadi.

Vercel'ga joylashtirib bo'lgach, KOMPYUTERINGIZDA shu skriptni bir marta
ishga tushirasiz. Undan keyin hech qachon qayta ishlatish shart emas -
Telegram o'sha manzilni doimiy eslab qoladi.

Ishlatish:
    BOT_TOKEN=... python3 setwebhook.py https://sizning-loyihangiz.vercel.app
"""
import sys
import os
import urllib.request
import urllib.parse
import json

if len(sys.argv) != 2:
    print("Ishlatish: python3 setwebhook.py https://loyiha-nomi.vercel.app")
    sys.exit(1)

BOT_TOKEN = os.environ["BOT_TOKEN"]
BASE_URL = sys.argv[1].rstrip("/")
WEBHOOK_URL = f"{BASE_URL}/api/webhook"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
data = urllib.parse.urlencode({"url": WEBHOOK_URL}).encode()
req = urllib.request.Request(url, data=data, method="POST")

with urllib.request.urlopen(req, timeout=10) as r:
    javob = json.loads(r.read())

if javob.get("ok"):
    print(f"Muvaffaqiyatli ulandi: {WEBHOOK_URL}")
else:
    print(f"XATO: {javob}")
    sys.exit(1)
