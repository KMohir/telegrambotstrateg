from aiogram import Router, types
from aiogram.filters import Command
from keyboards.keyboards import main_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Men Instagram kontent generator va trend analiz botman.\n\n"
        "Quyidagi bo'limlardan birini tanlang:",
        reply_markup=main_menu
    )
