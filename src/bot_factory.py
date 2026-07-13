from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession

from src.config.settings import settings
from src.handlers.chat_join_request_handler import build_chat_join_request_router
from src.handlers.chat_member_handler import build_chat_member_router
from src.handlers.check_handler import build_check_router
from src.handlers.my_chat_member_handler import build_my_chat_member_router
from src.handlers.start_handler import build_start_router
from src.repositories.subscriber_repository import SubscriberRepository
from src.services.messaging_service import MessagingService
from src.services.subscription_service import SubscriptionService


def create_application(subscriber_repository: SubscriberRepository):
    session = (
        AiohttpSession(proxy=settings.telegram_proxy_url)
        if settings.telegram_proxy_url
        else None
    )
    bot = Bot(
        token=settings.bot_token,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher()

    subscription_service = SubscriptionService(
        bot=bot,
        subscriber_repository=subscriber_repository,
    )

    messaging_service = MessagingService(
        bot=bot,
        subscriber_repository=subscriber_repository,
    )

    dispatcher.include_router(build_start_router(subscription_service))
    dispatcher.include_router(build_check_router(subscription_service, messaging_service))
    dispatcher.include_router(build_chat_join_request_router(bot, subscription_service, messaging_service))
    dispatcher.include_router(build_chat_member_router(subscription_service, messaging_service))
    dispatcher.include_router(build_my_chat_member_router(subscription_service))

    return bot, dispatcher
