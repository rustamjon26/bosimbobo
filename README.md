# Bosim Bobo Telegram Bot

Bosim Bobo restorani filiallari uchun Telegram bot. Foydalanuvchi filialni tanlaydi, bot lokatsiya va aloqa ma'lumotlarini yuboradi.

## Loyiha tuzilmasi

```
bosim-bobo-bot/
├── bot.py
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

## 1. Botni ishga tushirish

### Talablar

- Python 3.10 yoki undan yuqori
- Internet ulanishi

### Tez ishga tushirish (Windows)

`.env` da haqiqiy `BOT_TOKEN` bo'lishi kerak. Keyin:

**Git Bash:**

```bash
cd "d:/cyber/bosim bobo bot/bosim-bobo-bot"
bash run.sh
```

**CMD yoki PowerShell:** `run.bat` faylini ikki marta bosing yoki:

```powershell
cd "d:\cyber\bosim bobo bot\bosim-bobo-bot"
.\run.bat
```

> Windows da ko'pincha `python` va `pip` PATH da bo'lmaydi. `py` launcher ishlaydi — skriptlar avtomatik `venv` yaratadi.

### O'rnatish (qo'lda)

1. Loyiha papkasiga kiring:

   ```bash
   cd bosim-bobo-bot
   ```

2. Virtual muhit yarating:

   **Windows (Git Bash / CMD / PowerShell) — `py` ishlating:**

   ```bash
   py -3.12 -m venv venv
   venv/Scripts/python.exe -m pip install -r requirements.txt
   ```

   **PowerShell (aktivatsiya bilan):**

   ```powershell
   py -3.12 -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

   **macOS / Linux:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. `.env` faylini sozlang:

   ```bash
   copy .env.example .env
   ```

   macOS/Linux: `cp .env.example .env`

   `.env` ichida haqiqiy tokenni yozing:

   ```
   BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

4. Botni ishga tushiring:

   ```bash
   venv/Scripts/python.exe bot.py
   ```

   Yoki aktivatsiyadan keyin: `python bot.py`

   Konsolda `Bot ishga tushdi` xabari chiqishi kerak.

6. Telegramda botingizni oching va `/start` yuboring.

### Buyruqlar

| Buyruq   | Vazifa                                      |
|----------|---------------------------------------------|
| `/start` | Xush kelibsiz xabari va filial tugmalari     |
| `/help`  | Barcha filiallar ro'yxati (matn ko'rinishida) |

## 2. Token olish (@BotFather)

1. Telegramda [@BotFather](https://t.me/BotFather) ni oching.
2. `/newbot` buyrug'ini yuboring.
3. Bot uchun **nom** va **username** kiriting (username `bot` bilan tugashi kerak, masalan: `bosim_bobo_bot`).
4. BotFather sizga token beradi, masalan:

   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

5. Bu tokenni `.env` faylidagi `BOT_TOKEN=` qatoriga qo'ying.

**Mavjud bot tokenini ko'rish:** `/mybots` → botingizni tanlang → **API Token**.

> Tokenni hech kimga bermang va GitHubga yuklamang. Faqat `.env` faylida saqlang.

## 3. Railway.app ga deploy qilish

[Railway](https://railway.app) botni doimiy ishlaydigan serverda ushlab turadi (polling rejimi).

### 1-bosqich: Kodni GitHubga yuklash

1. [GitHub](https://github.com) da yangi repository yarating.
2. `bosim-bobo-bot` papkasidagi fayllarni yuklang.
3. `.env` faylini **yuklamang** — faqat `.env.example`.

### 2-bosqich: Railway loyihasi

1. [railway.app](https://railway.app) ga kiring va ro'yxatdan o'ting.
2. **New Project** → **Deploy from GitHub repo**.
3. Repositoryingizni tanlang.
4. Agar repo katta bo'lsa, **Root Directory** ni `bosim-bobo-bot` qilib belgilang.

### 3-bosqich: Muhit o'zgaruvchilari (Variables)

1. Service → **Variables** bo'limiga o'ting.
2. Yangi o'zgaruvchi qo'shing:

   | Nom         | Qiymat                    |
   |-------------|---------------------------|
   | `BOT_TOKEN` | BotFather dan olgan token |

3. Saqlang — Railway avtomatik qayta deploy qiladi.

### 4-bosqich: Ishga tushirish buyrug'i

1. **Settings** → **Deploy** bo'limiga o'ting.
2. **Start Command** maydoniga yozing:

   ```
   python bot.py
   ```

3. Build `requirements.txt` orqali avtomatik bajariladi.

### 5-bosqich: Tekshirish

1. **Deployments** → oxirgi deploy → **View Logs**.
2. Logda `Bot ishga tushdi` ko'rinsa, bot ishlayapti.
3. Telegramda `/start` yuborib sinab ko'ring.

### Muhim eslatmalar

- **Bitta nusxa** ishlating. Bir xil token bilan bir nechta server polling qilsa, xatoliklar chiqadi.
- HTTP webhook emas, **polling** ishlatiladi — Railway da doimiy ishlaydigan **Worker** xizmati kerak.
- Telefon va koordinatalarni `bot.py` ichidagi `BRANCHES` ro'yxatida yangilashingiz mumkin.

## Muammolarni hal qilish

| Muammo                         | Yechim                                              |
|--------------------------------|-----------------------------------------------------|
| `python: command not found`    | `py -3.12` yoki `bash run.sh` / `run.bat` ishlating |
| `BOT_TOKEN topilmadi`          | `.env` mavjudligi va token to'g'ri yozilganini tekshiring |
| Bot javob bermayapti           | `venv/Scripts/python.exe bot.py` ishlayotganini va token to'g'riligini tekshiring |
| Railway da bot to'xtaydi       | Start Command: `python bot.py` va loglarni ko'ring  |

## Texnologiyalar

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) 20.7 (async)
- [python-dotenv](https://github.com/theskumar/python-dotenv) 1.0.0
# bosimbobo
