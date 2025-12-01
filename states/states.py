from aiogram.fsm.state import State, StatesGroup

class ContentState(StatesGroup):
    topic = State()       # Mavzu
    audience = State()    # Auditoriya
    goal = State()        # Maqsad
    tone = State()        # Ohang (Tone of voice)
    format = State()      # Format (Reels, Post, Story)
    additional = State()  # Qo'shimcha ma'lumot

class TrendState(StatesGroup):
    keyword = State()     # Kalit so'z

