import random

from data import irregular_verbs
from keyboards import menu, tartib_keyboard, boshlash_button, toxtatish

from aiogram import F, Router
from aiogram.fsm import state
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery, ContentType



class States(state.StatesGroup):
    tar_tan = state.State(state="Tartibni tanlash")
    testda = state.State(state='Test bo\'lmoqda')


router = Router()

@router.message(Command(commands=['start', 'bosh_menu']))
async def start(msg : Message, state : FSMContext):
    await msg.answer(
        text=f"<b>Assalomu alaykum {msg.from_user.mention_html(msg.from_user.first_name)}</b>",
        reply_markup=menu,
    )
    await state.set_state()

@router.message(F.text == "⚡️Testni boshlash | Barchasidan⚡️", StateFilter(None))
async def tartib_bilan(msg : Message, state : FSMContext):
    await msg.answer(
        text=f"<b>Testlar soni : 10 ta\n\n<i>Testni boshlash uchun boshlash tugmasini bosing !</i></b>",
        reply_markup=boshlash_button(0)
    )

@router.message(F.text == "⚡️Testni boshlash | Tartib bilan⚡️", StateFilter(None))
async def barchasidan(msg : Message, state : FSMContext):
    await msg.answer(text="<b>Qaysi bo'limdan boshlaymiz ?</b>", reply_markup=tartib_keyboard())
    await state.set_state(States.tar_tan)

@router.message(F.text == "◀️ Ortga")
async def ortga(msg : Message, state : FSMContext):
    await msg.answer(
        text=f"Bosh menu :",
        reply_markup=menu,
    )
    await state.set_state()

@router.message(States.tar_tan, F.content_type == ContentType.TEXT)
async def tartib(msg : Message, state : FSMContext):
    if msg.text.isdigit() and int(msg.text) in range(1, 11):
        tartibi = int(msg.text)
        await msg.answer(
            text=f"<b>Testlar soni : 10 ta\n\n<i>Testni boshlash uchun boshlash tugmasini bosing !</i></b>",
            reply_markup=boshlash_button(tartibi)
        )
        await state.clear()
    else:
        await msg.answer(
            text="1 - 10 oralig'idagi son yuboring :",
            reply_markup=tartib_keyboard(),
        )
  
@router.callback_query(F.data.startswith("start"))
async def start_test(call : CallbackQuery, state : FSMContext):
    n = int(call.data.split(':')[1])
    if n == 0:
        data = random.sample(irregular_verbs, 10)
    else:
        data = irregular_verbs[10*n - 10 : 10*n]
    await call.answer("🪄 Test boshlandi 🪄")
    text = f"<b>❔ Fe'l : <i>{data[0]['infinitive']}</i>\n\n📝 Past simple ko'rinishini yuboring :</b>"
    await call.message.delete()
    await state.update_data({'tur': 'simple', 'data': data, 'tartib': 0})
    await call.message.answer(text, reply_markup=toxtatish)
    await state.set_state(States.testda)

@router.message(States.testda, F.text == "❌ Testni to'xtatish")
async def toxtatish_(msg : Message, state : FSMContext):
    await msg.answer(
        text="<b>Test to'xtatildi !\n\nMenu :</b>",
        reply_markup=menu
    )
    await state.clear()

@router.message(States.testda, F.text == "♻️ Keyingi savolga o'tish")
async def toxtatish_(msg : Message, state : FSMContext):
    data = await state.get_data()
    tests = data['data']
    tartib = data['tartib']
    tur = data['tur']
    
    if tur == 'simple':
        text = f"<b>✅ To'g'ri javob : <i>{tests[tartib]['past_simple']}</i>\n\n<i>📝 Past participle</i> ko'rinishini topishga harakat qiling :\n\n<i>❔ Fe'l : {tests[tartib]['infinitive']}</i></b>"
        await msg.answer(text, reply_markup=toxtatish)
        await state.update_data({'tur': 'participle'})
    elif tur == 'participle':
        if tartib != 9:
            text = f"<b>✅ To'g'ri javob : <i>{tests[tartib]['past_participle']}</i>\n\n❔ Keyingi fe'l : <i>{tests[tartib+1]['infinitive']}</i>\n\n📝 <i>Past simple</i> ko'rinishini yuboring :</b>"
            await msg.answer(text, reply_markup=toxtatish)
            await state.update_data({
                'tartib': tartib + 1,
                'tur': 'simple'
            })
        else:
            text = f"<b>✅ To'g'ri javob : <i>{tests[tartib]['past_participle']}</i>\n\n🪄 Test tugadi 🪄</b>"
            await msg.answer(text, reply_markup=menu)
            await state.clear()

@router.message(States.testda, F.content_type == ContentType.TEXT)
async def testdaa(msg : Message, state : FSMContext):
    data = await state.get_data()
    tests = data['data']
    tartib = data['tartib']
    tur = data['tur']
    javob = msg.text
    
    if tur == 'simple':
        if tests[tartib]['past_simple'] == javob:
            text = f"<b>Javobingiz to'g'ri ✅\n\n📝 Endi esa <i>Past participle</i> ko'rinishini yuboring :\n\n<i>❔ Fe'l : {tests[tartib]['infinitive']}</i></b>"
            await msg.answer(text, reply_markup=toxtatish)
            await state.update_data({'tur': 'participle'})
        else:
            await xato(msg)
    elif tur == 'participle':
        if tests[tartib]['past_participle'] == javob:
            if tartib != 9:
                text = f"<b>Javobingiz to'g'ri ✅\n\n❔ Keyingi fe'l : <i>{tests[tartib+1]['infinitive']}</i>\n\n📝 <i>Past simple</i> ko'rinishini yuboring :</b>"
                await msg.answer(text, reply_markup=toxtatish)
                await state.update_data({
                    'tartib': tartib + 1,
                    'tur': 'simple'
                })
            else:
                text = f"<b>Javobingiz to'g'ri ✅\n\nTestni tugatdingiz 🎉</b>"
                await msg.answer(text, reply_markup=menu)
                await state.clear()
        else:
            await xato(msg)

async def xato(msg: Message):
    await msg.answer(
        text="Javobingiz xato ❌",
        reply_markup=toxtatish
    )
