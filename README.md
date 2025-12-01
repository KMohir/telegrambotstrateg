# Instagram Content Generator & Trend Analysis Bot

Bu Telegram bot Instagram uchun kontent g'oyalar generatsiya qilish va trend videolarni tahlil qilish uchun mo'ljallangan.

## Xususiyatlari

1.  **Kontent Generator**:
    -   Foydalanuvchidan 6 ta savol so'raydi (Mavzu, Auditoriya, Maqsad, va h.k.).
    -   OpenAI (ChatGPT) yordamida 3 ta variantda (Hook, Body, CTA) ssenariy yaratadi.
    -   Qayta generatsiya qilish imkoniyati.

2.  **Trend Analiz**:
    -   Kalit so'z bo'yicha (masalan: "marketing", "biznes") trend videolarni qidiradi.
    -   Ko'rishlar, layklar va o'sish ko'rsatkichlarini taqdim etadi.

## O'rnatish

1.  Loyiha fayllarini yuklab oling.
2.  Virtual muhitni yarating va faollashtiring:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Kerakli kutubxonalarni o'rnating:
    ```bash
    pip install -r requirements.txt
    ```
4.  `.env` faylini yarating va API kalitlarni kiriting (namuna `.env.example` da):
    ```env
    BOT_TOKEN=sizning_bot_tokeningiz
    OPENAI_API_KEY=sizning_openai_kalitingiz
    RAPIDAPI_KEY=sizning_rapidapi_kalitingiz (ixtiyoriy)
    ```

## Ishga tushirish

```bash
source venv/bin/activate
python main.py
```

## Texnologiyalar

-   Python 3.x
-   aiogram 3.x
-   OpenAI API
-   Instagram Scraper API (RapidAPI)
