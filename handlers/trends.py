from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.states import TrendState
from services.insta_service import get_trend_videos
from aiogram.types import ReplyKeyboardRemove

router = Router()

@router.message(F.text == "📊 Trend videolarni topish")
async def start_trend_analysis(message: types.Message, state: FSMContext):
    await message.answer("Qaysi nisha bo'yicha trend videolar kerak? (Masalan: marketing, biznes, ai)", reply_markup=ReplyKeyboardRemove())
    await state.set_state(TrendState.keyword)

@router.message(TrendState.keyword)
async def process_keyword(message: types.Message, state: FSMContext):
    keyword = message.text
    await message.answer(f"🔎 '{keyword}' bo'yicha trendlar qidirilmoqda...")
    
    trends = await get_trend_videos(keyword)
    
    if not trends:
        await message.answer("Afsuski, hech narsa topilmadi.")
    else:
        response_text = f"🔥 '{keyword}' bo'yicha top trendlar:\n\n"
        for i, video in enumerate(trends, 1):
            response_text += (
                f"{i}. @{video['username']}\n"
                f"🎬 Video: {video['url']}\n"
                f"👁 {video['views']:,} views\n"
                f"❤ {video['likes']:,} likes\n"
                f"💬 {video['comments']:,} comments\n"
                f"📈 x{video['growth']} o'sish\n\n"
            )
        
        from keyboards.keyboards import main_menu
        await message.answer(response_text, reply_markup=main_menu)
    
    await state.clear()
