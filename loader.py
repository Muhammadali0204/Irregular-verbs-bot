from aiogram import Bot
from decouple import config
from aiogram.client.default import DefaultBotProperties



ADMIN = config('ADMIN')
BOT_TOKEN = config('BOT_TOKEN')
bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode="HTML",
        ),
    )

