from __future__ import annotations

import asyncio
import re
from datetime import datetime, timezone

from aiogram import Bot
from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.config.messages import get_welcome_message
from src.repositories.subscriber_repository import SubscriberRepository
from src.types.subscriber import Subscriber
from src.utils.logger import get_logger
from src.utils.telegram_utils import is_blocked_bot_error

logger = get_logger(__name__)


class MessagingService:
    def __init__(
        self,
        bot: Bot,
        subscriber_repository: SubscriberRepository,
    ):
        self.bot = bot
        self.subscriber_repository = subscriber_repository
        self._welcome_delivery_tasks: dict[int, asyncio.Task[bool]] = {}
        self._photo_file_ids: dict[str, str] = {}

    async def send_welcome_message(self, subscriber: Subscriber, welcome_source: str | None = None) -> bool:
        existing_task = self._welcome_delivery_tasks.get(subscriber.user_id)
        if existing_task is not None:
            return await existing_task

        task = asyncio.create_task(self._deliver_welcome_message(subscriber, welcome_source))
        self._welcome_delivery_tasks[subscriber.user_id] = task
        try:
            return await task
        finally:
            current_task = self._welcome_delivery_tasks.get(subscriber.user_id)
            if current_task is task:
                self._welcome_delivery_tasks.pop(subscriber.user_id, None)

    async def _deliver_welcome_message(self, subscriber: Subscriber, welcome_source: str | None = None) -> bool:
        sent_at = datetime.now(tz=timezone.utc)
        resolved_source = welcome_source or subscriber.welcome_source
        message_data = get_welcome_message(resolved_source)
        candidate_chat_ids = [subscriber.chat_id]

        if subscriber.user_id not in candidate_chat_ids:
            candidate_chat_ids.append(subscriber.user_id)

        for chat_id in candidate_chat_ids:
            try:
                await self._send_message_data(
                    chat_id=chat_id,
                    message_data=message_data,
                )
                await self.subscriber_repository.mark_welcome_sent(subscriber.user_id, sent_at)
                logger.info(
                    "Welcome message sent to user_id=%s chat_id=%s welcome_source=%s",
                    subscriber.user_id,
                    chat_id,
                    resolved_source,
                )
                return True
            except Exception as error:
                await self._handle_send_error(subscriber.user_id, error)
                logger.exception(
                    "Failed to send welcome message to user_id=%s chat_id=%s",
                    subscriber.user_id,
                    chat_id,
                )

        return False

    async def _send_message_data(
        self,
        chat_id: int,
        message_data: dict,
    ) -> None:
        buttons = message_data.get("buttons")
        if buttons is None and {"button_text", "button_url"} <= message_data.keys():
            buttons = [
                {
                    "text": message_data["button_text"],
                    "url": message_data["button_url"],
                }
            ]

        keyboard = None
        if buttons:
            keyboard_rows = [
                [InlineKeyboardButton(text=button["text"], url=button["url"])]
                for button in buttons
            ]
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)

        image_path = message_data.get("image_path")
        caption = message_data.get("caption", "")
        safe_caption = self._strip_custom_emoji_tags(caption)

        if image_path:
            try:
                await self._send_photo_message(
                    chat_id=chat_id,
                    image_path=image_path,
                    caption=caption,
                    keyboard=keyboard,
                )
                return
            except Exception:
                logger.warning(
                    "Failed to send photo to chat_id=%s image_path=%s, retrying as text-only",
                    chat_id,
                    image_path,
                    exc_info=True,
                )
                if safe_caption != caption:
                    try:
                        await self._send_photo_message(
                            chat_id=chat_id,
                            image_path=image_path,
                            caption=safe_caption,
                            keyboard=keyboard,
                        )
                        logger.info(
                            "Photo delivered to chat_id=%s using sanitized caption fallback",
                            chat_id,
                        )
                        return
                    except Exception:
                        logger.warning(
                            "Sanitized photo caption fallback failed for chat_id=%s image_path=%s",
                            chat_id,
                            image_path,
                            exc_info=True,
                        )

        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=caption,
                reply_markup=keyboard,
            )
        except Exception:
            if safe_caption == caption:
                raise

            logger.warning(
                "Failed to send message to chat_id=%s with custom emoji, retrying with sanitized caption",
                chat_id,
                exc_info=True,
            )
            await self.bot.send_message(
                chat_id=chat_id,
                text=safe_caption,
                reply_markup=keyboard,
            )

    async def _send_photo_message(
        self,
        chat_id: int,
        image_path: str,
        caption: str,
        keyboard: InlineKeyboardMarkup | None,
    ) -> None:
        cached_file_id = self._photo_file_ids.get(image_path)
        if cached_file_id is not None:
            try:
                await self.bot.send_photo(
                    chat_id=chat_id,
                    photo=cached_file_id,
                    caption=caption,
                    reply_markup=keyboard,
                )
                return
            except Exception:
                self._photo_file_ids.pop(image_path, None)
                logger.warning(
                    "Cached Telegram file_id failed for image_path=%s, uploading file again",
                    image_path,
                    exc_info=True,
                )

        photo = FSInputFile(image_path)
        sent_message: Message = await self.bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
            reply_markup=keyboard,
        )
        if sent_message.photo:
            self._photo_file_ids[image_path] = sent_message.photo[-1].file_id

    async def send_text(self, chat_id: int, text: str) -> None:
        await self.bot.send_message(chat_id, text)

    async def _handle_send_error(self, user_id: int, error: Exception) -> None:
        if is_blocked_bot_error(error):
            logger.info("Bot send failed because user_id=%s blocked the bot", user_id)

    def _strip_custom_emoji_tags(self, text: str) -> str:
        return re.sub(r"<tg-emoji\b[^>]*>(.*?)</tg-emoji>", r"\1", text, flags=re.DOTALL)
