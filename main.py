import asyncio
import logging
import sys
from loader import dp, bot
from handlers import start, content, trends

async def main():
    # Logging configuration
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    
    # Register routers
    dp.include_router(start.router)
    dp.include_router(content.router)
    dp.include_router(trends.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
