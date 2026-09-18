# -*- coding: utf-8 -*-
"""
YO'NALTIRUVCHI BOT - Vercel serverless funksiya sifatida.

Render'dagi polling (`while True`) usulidan farqli o'laroq, bu yerda
WEBHOOK ishlatiladi: funksiya doim ishlab TURMAYDI, faqat Telegram
xabar kelganda BIR MARTA chaqiriladi va darhol tugaydi.

Shuning uchun "uxlab qolish" degan narsa BU YERDA umuman yo'q - chunki
doim ishlab turadigan jarayonning o'zi yo'q. Vercel'ning bepul tarifi
buni cheksiz qo'llab-quvvatlaydi.
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error

BOT_TOKEN = os.environ["BOT_TOKEN"]      # ESKI token shu yerga qo'yiladi
YANGI_BOT = os.environ.get("YANGI_BOT", "@Zabongo_Bot")

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

XABAR = (
    "Assalomu alaykum! 👋\n\n"
    "Ilovamiz yangi manzilga ko'chdi.\n\n"
    f"👉 {YANGI_BOT}\n\n"
    "Barcha ma'lumotlaringiz, tangalaringiz va reytingingiz to'liq "
    "saqlanib qolgan - yangi botni oching va xuddi shu joyingizdan "
    "davom eting."
)


def send(chat_id):
    req = urllib.request.Request(
        f"{API}/sendMessage",
        data=json.dumps({"chat_id": chat_id, "text": XABAR}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.status


def process_update(update: dict):
    """
    Telegram'dan kelgan bitta yangilikni qayta ishlaydi.

    Sinash uchun HTTP qismidan ATAYLAB ajratilgan - shunda haqiqiy
    tarmoqqa chiqmasdan mantiqni tekshirish mumkin.
    """
    msg = update.get("message")
    if not msg:
        # `my_chat_member` (blok/blokdan chiqarish) e'tiborga olinmaydi -
        # bloklagan odamga yozib bo'lmaydi, faqat keraksiz xato bo'ladi.
        return None
    chat_id = (msg.get("chat") or {}).get("id")
    if not chat_id:
        return None
    try:
        send(chat_id)
        return chat_id
    except urllib.error.URLError as e:
        print(f"Yuborishda xato ({chat_id}): {e}")
        return None


class handler(BaseHTTPRequestHandler):
    """Vercel Python funksiyalari shu nom bilan sinfni kutadi: `handler`."""

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b""
        try:
            update = json.loads(raw or b"{}")
        except json.JSONDecodeError:
            update = {}

        process_update(update)

        body = b'{"ok":true}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        # Brauzerdan ochib ko'rish uchun - shunchaki tirik ekanini bildiradi
        body = b'{"status":"yo\'naltiruvchi bot ishlayapti"}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
