from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎥 Kontent yaratish"),
            KeyboardButton(text="📊 Trend videolarni topish")
        ]
    ],
    resize_keyboard=True
)
