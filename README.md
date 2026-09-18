# Yo'naltiruvchi bot (Vercel, webhook)

Eski @Koreystili40kunda_bot tokeni uchun. Yagona vazifasi: kimdir yozsa,
yangi bot manzilini aytadi.

Bu versiya WEBHOOK ishlatadi (Render'dagi polling emas) - shuning uchun
Vercel'ning bepul serverless funksiyalarida ishlaydi, "uxlab qolish"
degan muammo umuman yo'q.

## Joylashtirish

1. Bu papkani GitHub'ga yuklang (Render uchun tayyorlagan repozitoriyingizdan
   alohida, yoki o'sha repoda saqlab, Vercel'ga faqat shu papkani ko'rsating)
2. https://vercel.com ga kiring, "Add New Project", GitHub repongizni tanlang
3. Vercel loyihani avtomatik taniydi (papkada `api/` borligini ko'radi)
4. **Settings → Environment Variables** ga ikkitasini qo'shing:
   - `BOT_TOKEN` - ESKI token (@Koreystili40kunda_bot)
   - `YANGI_BOT` - `@Zabongo_Bot`
5. Deploy qiling - loyiha manzili shunday bo'ladi: `https://loyiha-nomi.vercel.app`

## Telegram'ga ulash (BIR MARTALIK)

Kompyuteringizda, terminalda:

```bash
BOT_TOKEN="eski_tokeningiz" python3 setwebhook.py https://loyiha-nomi.vercel.app
```

"Muvaffaqiyatli ulandi" chiqsa - tayyor. Buni qayta ishlatish shart emas.

## Sinash

@Koreystili40kunda_bot ga `/start` yozing - darhol yo'naltiruvchi xabar kelishi kerak.
