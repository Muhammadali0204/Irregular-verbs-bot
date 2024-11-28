from app import dp
from loader import bot
from data import irregular_verbs

from aiogram import F
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from keyboards import menu, tartib_keyboard
from aiogram.types import Message, CallbackQuery, ContentType




class States(state.StatesGroup):
    tar_tan = state.State(state="Tartibni tanlash")


@dp.message(Command(commands=['start', 'bosh_menu']))
async def start(msg : Message, state : FSMContext):
    await msg.answer(
        text=f"Assalomu alaykum {msg.from_user.mention_html(msg.from_user.first_name)}",
        reply_markup=menu,
    )
    await state.set_state()
    

@dp.message(F.text == "Testni boshlash | Barchasidan")
async def start(msg : Message, state : FSMContext):
    await msg.answer(text="<b>Qaysi bo'limdan boshlaymiz ?</b>", reply_markup=tartib_keyboard())
    await state.set_state(States.tar_tan)
    
@dp.message(States.tar_tan, F.content_type == ContentType.TEXT)
async def tartib(msg : Message, state : FSMContext):
    pass
  
@dp.message(F.text == "Testni boshlash | Tartib bilan")
async def start():
    pass
