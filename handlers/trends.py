from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.states import TrendState
from services.insta_service import get_trend_videos
from services.openai_service import analyze_video_caption
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

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
        await state.clear()
    else:
        # Store trends in state for later analysis
        await state.update_data(trends=trends)
        
        response_text = f"🔥 '{keyword}' bo'yicha top trendlar:\n\n"
        
        # Create inline keyboard for video selection
        keyboard_buttons = []
        
        for i, video in enumerate(trends, 1):
            response_text += (
                f"{i}. @{video['username']}\n"
                f"🎬 Video: {video['url']}\n"
                f"👁 {video['views']:,} views\n"
                f"❤ {video['likes']:,} likes\n"
                f"💬 {video['comments']:,} comments\n\n"
            )
            
            # Add button for each video
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text=f"📊 {i}-videoni tahlil qilish",
                    callback_data=f"analyze_{i-1}"
                )
            ])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        from keyboards.keyboards import main_menu
        await message.answer(response_text, reply_markup=keyboard)
        await message.answer("Videoni tahlil qilish uchun tugmani bosing:", reply_markup=main_menu)
        
        await state.set_state(TrendState.analyzing)

@router.callback_query(F.data.startswith("analyze_"))
async def analyze_video(callback: types.CallbackQuery, state: FSMContext):
    # Get video index from callback data
    video_index = int(callback.data.split("_")[1])
    
    # Get trends from state
    data = await state.get_data()
    trends = data.get("trends", [])
    
    if video_index >= len(trends):
        await callback.answer("Xatolik: Video topilmadi")
        return
    
    video = trends[video_index]
    
    await callback.answer("⏳ Tahlil qilinmoqda...")
    await callback.message.answer("⏳ Video tahlil qilinmoqda, iltimos kuting...")
    
    # Analyze the video caption
    analysis = await analyze_video_caption(
        caption=video.get("caption", ""),
        username=video.get("username", ""),
        views=video.get("views", 0),
        likes=video.get("likes", 0)
    )
    
    # Send analysis result
    await callback.message.answer(f"📊 **Video tahlili:**\n\n{analysis}")
    
    await state.clear()
