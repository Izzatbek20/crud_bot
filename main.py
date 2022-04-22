import logging

from aiogram import Bot, Dispatcher, executor, types

from aiogram.utils.callback_data import CallbackData

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

#tokken
API_TOKEN = ''

# ADMIN ID
# ADMIN_ID = 1733819468
ADMIN_ID = 1057006280

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# inline menyu uchun action
posts_cb = CallbackData('post', 'id', 'action')
# inline menyu uchun action

# ariza toldirish uchun forma
class Form(StatesGroup):
    project = State()
    name = State()
    phone = State()
    aloqa = State()
# ariza toldirish uchun forma

#button
btn = types.InlineKeyboardMarkup()
btn.row(
    types.InlineKeyboardButton('Ussd',  callback_data=posts_cb.new(action='project', id='ussd')),
    types.InlineKeyboardButton('Boshqalar',  callback_data=posts_cb.new(action='project', id='boshqa'))
)
btn_menu_bekor_qilish = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(types.KeyboardButton('❌ Arizani bekor qilish'))

btn_menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).row(
    types.KeyboardButton('ℹ️ Biz haqimizda'),
    types.KeyboardButton('📞 Aloqa')
).row(
    types.KeyboardButton('📍 Manzil'),
    types.KeyboardButton('🗒 Loyihalar'),
)
# button

#arizai bekor qilish
@dp.message_handler(lambda message: message.text in ["❌ Arizani bekor qilish"], state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()

    await state.finish()
    await message.answer('Bekor qilindi.', reply_markup=btn_menu)

@dp.message_handler(lambda message: message.text in ["ℹ️ Biz haqimizda"])
async def cancel_handler(message: types.Message):
    text = "Only Up Jamoasi haqida:\n\nOnly Up Jamoasi  eng yosh kompaniyalardan biri bo'lib, qisqa muddat ichida 🇺🇿  O'zbekistonda va 🌐 Xorijda o'zining loyihalarini amalga oshirib kelayotgan kam sonli kompanyalardan biri." \
           "\n\n📋 Bo'limlar:" \
           "\n\n💻 Web dasturlash(Front End):bu bo'limda o'z biznesingiz uchun hech bir internet satiga o'xshamas web sahifaga buyurtma berishingiz mumkin." \
           "\n\n🛠 Qo'llaniladigan texnologiyalar: HTML5, CSS3, Bootstrap4, Javascript, jQuery" \
           "\n\n💻 Web dasturlash(Beck End):bu bo'limda Front End bo'limda yasalgan intrnet sahifalarning logikasini qanday bo'lishini bilib olishingiz mumkin." \
           "\n\n🛠 Qo'llaniladigan texnologiyalar: Javascript, jQuery, PHP, MySQL, Git, Yii2/Laravel" \
           "\n\n📱 Mobile dasturlash(Android):bu bo'limda Android operatsion tizimida ishlovchi barcha qurilmalarga dasturlarga buyurtma qilishingiz mumkin." \
           "\n\n🛠 Qo'llaniladigan texnologiyalar: Android Studio, Kotlin, Java"
    await message.answer(text, reply_markup=btn_menu)

@dp.message_handler(lambda message: message.text in ["📞 Aloqa"])
async def cancel_handler(message: types.Message):
    text = "Biz bilan bog'lanish:" \
           "\n\n📞 Tel.: +998(33) 110 00 33 "\
           "\n🌐 Sayt: https://crud.uz/" \
           "\n\nIjtimoiy tarmoqlar:" \
           "\nTelegram: t.me/crud_group_uz" \
           "\nInstagram: instagram.com/crud_group_uz"
    await message.answer(text, reply_markup=btn_menu)

@dp.message_handler(lambda message: message.text in ["📍 Manzil"])
async def cancel_handler(message: types.Message):
    await message.answer_location('40.3869023', '71.7832996')\

@dp.message_handler(lambda message: message.text in ["🗒 Loyihalar"])
async def cancel_handler(message: types.Message):
    await message.answer('Quyidagi menyu orqali o`zingizga qiziq bo`lgan loyihani tanlang.', reply_markup=btn)
#arizai bekor qilish


#start==========================================================================================================================================
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    # if ADMIN_ID == message.from_user.id:
    #     await message.answer(f"Assalomu alaykum, {message.from_user.full_name}")
    # else:
    text = f"Assalomu alaykum, {message.from_user.full_name}\n\nCRUD Group botga xush kelibsiz!"
    await message.answer(text, reply_markup=btn_menu)
#start==================================================================================================================================


#ariza toldirish =============================================================================================================================
@dp.callback_query_handler(posts_cb.filter(action='project'))
async def users_db(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    value = str(callback_data['id'])
    await Form.project.set()
    async with state.proxy() as data:
        data['project'] = value
    await bot.send_message(query.from_user.id, 'Biz bilan muloqot qilish uchun 📄 o`zingiz haqingizda ma`lumot qoldiring!')
    await Form.next()
    return await bot.send_message(query.from_user.id, 'Ismingiz?',  reply_markup=btn_menu_bekor_qilish)

@dp.message_handler(state=Form.name)
async def name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Form.next()
    return await message.answer("Telefon raqamingiz?", reply_markup=btn_menu_bekor_qilish)

@dp.message_handler(state=Form.phone)
async def name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    await Form.next()
    return await message.answer("O`zingiga qulay bo`lgan vaqtni kiriting va biz siz bilan bog`lanamiz", reply_markup=btn_menu_bekor_qilish)

@dp.message_handler(state=Form.aloqa)
async def name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['aloqa'] = message.text
    await state.finish()
    text = f"Project: <b>{data['project']}</b>\n\nIsm: <b>{data['name']}</b>\nTelefon: <b>{data['phone']}</b>\nAloqa vaqti: <b>{data['aloqa']}</b>\n\n<i>User name: {message.from_user.full_name}\nUser id: {message.from_user.id}</i>"
    text_users = f"Project: <b>{data['project']}</b>\n\nIsm: <b>{data['name']}</b>\nTelefon: <b>{data['phone']}</b>\nAloqa vaqti: <b>{data['aloqa']}</b>\n\nBu vaqt oralig`ida hodimlarimiz siz bilan bog`lanishadi!"
    await bot.send_message(ADMIN_ID, text, parse_mode='HTML')
    await bot.send_message(message.from_user.id, text_users, reply_markup=btn_menu, parse_mode='HTML')
#ariza toldirish =========================================================================================================================





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
