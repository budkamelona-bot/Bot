import asyncio

from src.bot_factory import create_application
from src.db.pool import create_pool, initialize_database
from src.repositories.subscriber_repository import SubscriberRepository
from src.utils.logger import get_logger, setup_logging

logger = get_logger(__name__)


async def main() -> None:
    setup_logging()

    pool = await create_pool()
    await initialize_database(pool)
    subscriber_repository = SubscriberRepository(pool)
    bot, dispatcher = create_application(subscriber_repository)
    logger.info("Bot started successfully")

    try:
        await dispatcher.start_polling(
            bot,
            allowed_updates=["message", "chat_member", "my_chat_member", "chat_join_request"],
        )
    finally:
        await bot.session.close()
        await pool.close()


if __name__ == "__main__":
    asyncio.run(main())
