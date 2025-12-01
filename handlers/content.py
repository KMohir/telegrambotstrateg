from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.states import ContentState
from services.openai_service import generate_content_ideas
from services.supabase_service import save_user_answers
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

router = Router()

# Global handlers (must be before state handlers)
@router.message(F.text == "🏠 Bosh menyu")
async def back_to_main(message: types.Message, state: FSMContext):
    await state.clear()
    from keyboards.keyboards import main_menu
    await message.answer("Bosh menyu", reply_markup=main_menu)

@router.message(F.text == "🔄 Qayta generatsiya qilish")
async def regenerate_content(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if not data or 'topic' not in data:
        await message.answer("Avval kontent yaratish bo'limidan o'ting.")
        return

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔄 Qayta generatsiya qilish")],
            [KeyboardButton(text="🏠 Bosh menyu")]
        ],
        resize_keyboard=True
    )

    await message.answer("⏳ Qayta generatsiya qilinmoqda...")
    result = await generate_content_ideas(data)
    await message.answer(result, reply_markup=kb)

# Content generation flow
@router.message(F.text == "🎥 Kontent yaratish")
async def start_content_gen(message: types.Message, state: FSMContext):
    await message.answer("Ajoyib! Kontent yaratish uchun bir nechta savollarga javob bering.\n\n1. Videoning asosiy mavzusi nima?", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ContentState.topic)

@router.message(ContentState.topic)
async def answer_topic(message: types.Message, state: FSMContext):
    await state.update_data(topic=message.text)
    await message.answer("2. Bu video kimlar uchun mo'ljallangan (Auditoriya)?")
    await state.set_state(ContentState.audience)

@router.message(ContentState.audience)
async def answer_audience(message: types.Message, state: FSMContext):
    await state.update_data(audience=message.text)
    await message.answer("3. Videodan ko'zlangan asosiy maqsad nima? (Sotuv, Obunachi yig'ish, Brendni tanitish va h.k.)")
    await state.set_state(ContentState.goal)

@router.message(ContentState.goal)
async def answer_goal(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await message.answer("4. Video qanday ohangda bo'lishi kerak? (Jiddiy, Hazil, Motivatsion, Ta'limiy)")
    await state.set_state(ContentState.tone)

@router.message(ContentState.tone)
async def answer_tone(message: types.Message, state: FSMContext):
    await state.update_data(tone=message.text)
    await message.answer("5. Video formati qanday? (Talking head, Voiceover, Trend, Sketch)")
    await state.set_state(ContentState.format)

@router.message(ContentState.format)
async def answer_format(message: types.Message, state: FSMContext):
    await state.update_data(format=message.text)
    await message.answer("6. Qo'shimcha istaklar yoki ma'lumotlar bormi? (Agar yo'q bo'lsa 'Yo'q' deb yozing)")
    await state.set_state(ContentState.additional)

@router.message(ContentState.additional)
async def answer_additional(message: types.Message, state: FSMContext):
    await state.update_data(additional=message.text)
    data = await state.get_data()
    
    await message.answer("⏳ Iltimos kuting, g'oyalar generatsiya qilinmoqda...")
    
    # Save to Supabase
    await save_user_answers(message.from_user.id, data)
    
    result = await generate_content_ideas(data)
    
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔄 Qayta generatsiya qilish")],
            [KeyboardButton(text="🏠 Bosh menyu")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(result, reply_markup=kb)
    await state.clear()  # Clear state after showing results
