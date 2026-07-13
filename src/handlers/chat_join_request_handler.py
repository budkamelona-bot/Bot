import asyncio

from aiogram import Bot, Router
from aiogram.types import ChatJoinRequest

from src.config.messages import resolve_welcome_source
from src.config.settings import settings
from src.services.messaging_service import MessagingService
from src.services.subscription_service import SubscriptionService
from src.utils.logger import get_logger

logger = get_logger(__name__)


def build_chat_join_request_router(
    bot: Bot,
    subscription_service: SubscriptionService,
    messaging_service: MessagingService,
) -> Router:
    router = Router()

    @router.chat_join_request()
    async def chat_join_request_handler(join_request: ChatJoinRequest) -> None:
        logger.info(
            "Join request received: request_chat_id=%s expected_channel_id=%s user_id=%s user_chat_id=%s username=%s",
            join_request.chat.id,
            settings.channel_id,
            join_request.from_user.id,
            join_request.user_chat_id,
            join_request.from_user.username,
        )

        if join_request.chat.id != settings.channel_id:
            logger.info(
                "Join request ignored because chat_id does not match target channel: request_chat_id=%s expected_channel_id=%s",
                join_request.chat.id,
                settings.channel_id,
            )
            return

        user = join_request.from_user
        invite_link = join_request.invite_link.invite_link if join_request.invite_link is not None else None
        invite_link_name = join_request.invite_link.name if join_request.invite_link is not None else None
        welcome_source = resolve_welcome_source(invite_link=invite_link, invite_link_name=invite_link_name)
        subscriber = None

        try:
            subscriber = await subscription_service.upsert_private_user(
                user_id=user.id,
                chat_id=join_request.user_chat_id,
                username=user.username,
                first_name=user.first_name,
                welcome_source=welcome_source,
            )

            await subscription_service.activate_subscription(user.id)

            logger.info(
                "Subscriber saved from join request: user_id=%s chat_id=%s invite_link=%s welcome_source=%s",
                user.id,
                join_request.user_chat_id,
                invite_link,
                welcome_source,
            )
        except Exception:
            logger.exception(
                "Failed to save subscriber from join request for user_id=%s",
                user.id,
            )

        welcome_task = None
        if subscriber is not None:
            welcome_task = asyncio.create_task(
                messaging_service.send_welcome_message(subscriber, welcome_source=welcome_source)
            )

        try:
            await bot.approve_chat_join_request(
                chat_id=join_request.chat.id,
                user_id=user.id,
            )
            logger.info(
                "Join request approved successfully: user_id=%s channel_id=%s",
                user.id,
                join_request.chat.id,
            )
        except Exception:
            logger.exception(
                "Failed to approve join request for user_id=%s channel_id=%s",
                user.id,
                join_request.chat.id,
            )

        if welcome_task is not None:
            sent = await welcome_task
            if not sent:
                logger.warning(
                    "Welcome message was not delivered from join request flow for user_id=%s welcome_source=%s",
                    user.id,
                    welcome_source,
                )

    return router
