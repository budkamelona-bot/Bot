import asyncio

from aiogram import Router
from aiogram.types import ChatMemberUpdated

from src.config.messages import resolve_welcome_source
from src.config.settings import settings
from src.services.messaging_service import MessagingService
from src.services.subscription_service import SubscriptionService
from src.utils.logger import get_logger
from src.utils.telegram_utils import is_active_member_status

logger = get_logger(__name__)


def build_chat_member_router(
    subscription_service: SubscriptionService,
    messaging_service: MessagingService,
) -> Router:
    router = Router()

    @router.chat_member()
    async def chat_member_handler(event: ChatMemberUpdated) -> None:
        if event.chat.id != settings.channel_id:
            return

        user = event.new_chat_member.user
        old_status = event.old_chat_member.status
        new_status = event.new_chat_member.status

        was_active = is_active_member_status(old_status)
        is_active = is_active_member_status(new_status)
        invite_link = event.invite_link.invite_link if event.invite_link is not None else None
        invite_link_name = event.invite_link.name if event.invite_link is not None else None
        welcome_source = resolve_welcome_source(invite_link=invite_link, invite_link_name=invite_link_name)
        via_join_request = bool(event.via_join_request)

        if not was_active and is_active:
            existing_subscriber = await subscription_service.find_by_user_id(user.id)
            chat_id = existing_subscriber.chat_id if existing_subscriber is not None else user.id

            await subscription_service.upsert_private_user(
                user_id=user.id,
                chat_id=chat_id,
                username=user.username,
                first_name=user.first_name,
                welcome_source=welcome_source,
            )
            await subscription_service.activate_subscription(user.id)

            subscriber = await subscription_service.find_by_user_id(user.id)
            should_send_welcome = subscriber is not None and (
                not via_join_request or subscriber.welcome_sent_at is None
            )
            sent = False
            if subscriber is not None and should_send_welcome:
                sent = await messaging_service.send_welcome_message(subscriber, welcome_source=welcome_source)
                if not sent and via_join_request:
                    await asyncio.sleep(0.5)
                    refreshed_subscriber = await subscription_service.find_by_user_id(user.id)
                    if refreshed_subscriber is not None and refreshed_subscriber.welcome_sent_at is None:
                        sent = await messaging_service.send_welcome_message(
                            refreshed_subscriber,
                            welcome_source=welcome_source,
                        )

            logger.info(
                "Channel subscription detected via chat_member for user_id=%s invite_link=%s welcome_source=%s via_join_request=%s should_send_welcome=%s sent=%s",
                user.id,
                invite_link,
                welcome_source,
                via_join_request,
                should_send_welcome,
                sent,
            )
            return

        if was_active and not is_active:
            await subscription_service.deactivate_subscription(user.id)
            await subscription_service.reset_delivery_state(user.id)
            logger.info("Channel unsubscribe detected via chat_member for user_id=%s", user.id)

    return router
