# -*- coding: utf-8 -*-
"""
YO'NALTIRUVCHI BOT - @Koreystili40kunda_bot uchun.

Vazifasi FAQAT bitta: eski botga yozgan har bir odamga "yangi manzilimiz
shu" deb aytish. Hech qanday baza, hech qanday dars, hech qanday murakkablik
yo'q - shuning uchun hozirgi katta dasturga tegmaydi va uni buzish xavfi yo'q.

Render'da BUTUNLAY ALOHIDA xizmat sifatida ishlaydi. Eski bot tokeni shu
yerga ulanadi, hozirgi katta dastur esa yangi tokenga o'tadi.
"""
import os
import time
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]  # ESKI token shu yerga qo'yiladi
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
    try:
        requests.post(f"{API}/sendMessage", json={
            "chat_id": chat_id,
            "text": XABAR,
        }, timeout=10)
    except requests.RequestException as e:
        print(f"Yuborishda xato ({chat_id}): {e}")


def poll_loop():
    """
    Telegram'ning eng oddiy usuli - long polling. Webhook, server,
    domen kerak emas: bot Render'da tinimsiz ishlab, Telegram'dan
    "kimdir yozdimi?" deb so'rab turadi.
    """
    offset = 0
    print("Yo'naltiruvchi bot ishga tushdi.")
    while True:
        try:
            r = requests.get(f"{API}/getUpdates", params={
                "offset": offset, "timeout": 30,
            }, timeout=35)
            r.raise_for_status()
            updates = r.json().get("result", [])
            for u in updates:
                offset = u["update_id"] + 1
                # FAQAT haqiqiy xabarlarga javob beramiz. `my_chat_member`
                # botni bloklash/blokdan chiqarish holatida ham keladi -
                # o'sha paytda yuborish shart emas (bloklagan odamga
                # baribir yetib bormaydi, faqat keraksiz xato bo'ladi).
                msg = u.get("message")
                if not msg:
                    continue
                chat_id = (msg.get("chat") or {}).get("id")
                if chat_id:
                    send(chat_id)
        except requests.RequestException as e:
            print(f"So'rovda xato: {e}")
            time.sleep(5)


if __name__ == "__main__":
    poll_loop()
