from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⚡️Testni boshlash | Tartib bilan⚡️"),
        ],
        [
            KeyboardButton(text="⚡️Testni boshlash | Barchasidan⚡️")
        ],
    ], resize_keyboard=True
)

toxtatish = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="♻️ Keyingi savolga o'tish")
        ],
        [
            KeyboardButton(text="❌ Testni to'xtatish")
        ]
    ],
    resize_keyboard=True
)

def tartib_keyboard():
    tartiblar = ReplyKeyboardBuilder()
    
    for i in range(1, 11):
        tartiblar.button(text=str(i))
    tartiblar.button(text="◀️ Ortga")
    tartiblar.adjust(3)
    
    return tartiblar.as_markup()

def boshlash_button(n : int):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🚀 Boshlash", callback_data=f'start:{n}')
            ]
        ]
    )
    
    return keyboard
