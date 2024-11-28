from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Testni boshlash | Tartib bilan"),
        ],
        [
            KeyboardButton(text="Testni boshlash | Barchasidan")
        ],
    ], resize_keyboard=True
)

def tartib_keyboard():
    tartiblar = ReplyKeyboardBuilder()
    
    for i in range(1, 11):
        tartiblar.button(text=i)
    tartiblar.adjust(3)
    
    return tartiblar.as_markup()
