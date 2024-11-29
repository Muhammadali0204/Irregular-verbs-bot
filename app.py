import contextlib, asyncio

from aiogram import Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from main import router
from loader import bot, ADMIN



async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    
    await bot.send_message(ADMIN, "<b>Bot ishga tushdi !</b>")
    
    await bot.set_my_commands(commands=[
        types.BotCommand(command='start', description='Botni ishga tushurish'),
        types.BotCommand(command='bosh_menu', description='Bosh menu'),
    ])
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
