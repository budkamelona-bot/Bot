from pathlib import Path
from urllib.parse import urlparse

PROJECT_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"

SOURCE_TIKTOK = "tiktok"
SOURCE_TIKTOK_NORM = "tiktok_norm"
SOURCE_YOUTUBE = "youtube"

TIKTOK_INVITE_LINK = "https://telegram.me/+QvKrFcrm3Ow0YjY6"
TIKTOK_NORM_INVITE_LINK = "https://t.me/+Dh7BGrFXon1hZGE6"
YOUTUBE_INVITE_LINK = "https://telegram.me/+_wPQMCnnhrA1Y2Uy"
UPCLICK_URL = "https://upclick.site/tzxlvrpmi"
SPINTO_URL = "https://megaslotsmatch.com/l/6a4ec0d6dda4f5282f0d2cb2"
NORM_URL = "https://gonormaff.com/?serial=61358616&creative_id=7675"
NORM_URL_HTML = NORM_URL.replace("&", "&amp;")

TG_PURPLE_HEART = '<tg-emoji emoji-id="5402366352042252021">💜</tg-emoji>'
TG_CHECK = '<tg-emoji emoji-id="5337160532216526521">✅</tg-emoji>'
TG_NEW = '<tg-emoji emoji-id="5458526506886124915">🆕</tg-emoji>'
TG_BROWN = '<tg-emoji emoji-id="5458430926683905591">🟫</tg-emoji>'
TG_MONEY = '<tg-emoji emoji-id="5391292736647209211">💸</tg-emoji>'
TG_GIFT = '<tg-emoji emoji-id="5203996991054432397">🎁</tg-emoji>'
TG_LIGHTNING = '<tg-emoji emoji-id="5456140674028019486">⚡</tg-emoji>'
TG_UPX = '<tg-emoji emoji-id="5377366193520781414">UP-X</tg-emoji>'
TG_SEPARATOR = '<tg-emoji emoji-id="5416117059207572332">:</tg-emoji>'
TG_NORM_HUNDRED = '<tg-emoji emoji-id="5274195706066781810">💯</tg-emoji>'
TG_NORM_FIRE = '<tg-emoji emoji-id="5420315771991497307">🔥</tg-emoji>'
TG_NORM_DIAMOND = '<tg-emoji emoji-id="5242679979078086072">💎</tg-emoji>'
TG_NORM_PROMO_GIFT = '<tg-emoji emoji-id="5192720653203031186">🎁</tg-emoji>'
TG_NORM_LINK = '<tg-emoji emoji-id="5330519486279740988">🌟</tg-emoji>'
TG_NORM_ARROW = '<tg-emoji emoji-id="5330131564833568029">🌟</tg-emoji>'
TG_NORM_END = '<tg-emoji emoji-id="5240038612845755187">🍭</tg-emoji>'
UPX_LINK_PREFIX = "UP-X:"

DEFAULT_WELCOME_MESSAGE = {
    "image_path": str(ASSETS_DIR / "random_message_1.jpg"),
    "caption": """
<b>ВСЕ ИГРЫ ИЗ ВИДЕО ТУТ</b>

🔥 MINESLOT 2 (NEW) — <a href="https://clck.ru/3QbX4Q">ИГРАТЬ</a>
🏎️ RUSH HOUR (МАШИНЫ) — <a href="https://clck.ru/3QbX4Q">ИГРАТЬ</a>
🎣 ICE FISHING (РЫБАЛКА) — <a href="https://clck.ru/3QbX4Q">ИГРАТЬ</a>

{TG_GIFT} <i>КРУТИ КОЛЕСО И ЗАБИРАЙ ДО 80.000₽ НА БАЛАНС К ДЕПОЗИТУ:</i>

💯 Вноси депозит и получай бонус: <b><u>250FS + 425% к пополнениям</u></b> 🧊
""".strip(),
}

TIKTOK_WELCOME_MESSAGE = {
    "image_path": str(PROJECT_DIR / "tiktok.jpg"),
    "caption": f"""
<b>ТА САМАЯ ИГРА ИЗ ТИК ТОКА — МАЙНКРАФТ</b> {TG_BROWN}

В этой игре тебе предстоит прокачивать свою кирку, чтобы собрать как можно больше кеша! {TG_MONEY}

{TG_GIFT} <b>100FS в Le Bandit ЗА ПЕРВЫЙ ДЕПОЗИТ</b> {TG_LIGHTNING}

📝 <b>Условия:</b>
🎰 Ставка: <b>40 RUB</b>
💰 Депозит: <b>от 1000 RUB</b>
🍀 Вейджер: <b>x3</b>

👇 <b>НИЖЕ ССЫЛКА ГДЕ МОЖНО ПОИГРАТЬ</b> 👇
{UPX_LINK_PREFIX} <a href="{UPCLICK_URL}">{UPCLICK_URL}</a>
{UPX_LINK_PREFIX} <a href="{UPCLICK_URL}">{UPCLICK_URL}</a>
""".strip(),
}

TIKTOK_NORM_WELCOME_MESSAGE = {
    "image_path": str(PROJECT_DIR / "new.jpg"),
    "caption": f"""
{TG_GIFT}<b>300FS НА НОВОМ ПРОЕКТЕ</b>{TG_NORM_HUNDRED}

{TG_NORM_FIRE}<b>Здесь ты найдешь :</b> {TG_NORM_FIRE}

{TG_NORM_DIAMOND}WELCOME PACK 225 % + 1000 FS
{TG_NORM_DIAMOND}Ежедневный кешбэк до 15%
{TG_NORM_DIAMOND}Моментальные выводы
{TG_NORM_DIAMOND}Круглосуточная поддержка
{TG_NORM_DIAMOND}Нет верификации

{TG_NORM_PROMO_GIFT} Вводи мой промо код <b>BUDKA</b> и забери
свои <b>300FS + 100%</b> к первому депозиту !

{TG_NORM_LINK} <b>NORM</b> {TG_NORM_ARROW} <a href="{NORM_URL_HTML}">{NORM_URL_HTML}</a>

Не упусти свой шанс стать частью истории
<b>NORM</b> {TG_NORM_END}
""".strip(),
}

YOUTUBE_WELCOME_MESSAGE = {
    "image_path": str(PROJECT_DIR / "youtube.jpg"),
    "caption": f"""
{TG_PURPLE_HEART} <b>ПРЯМО СЕЙЧАС ЗАБИРАЙ 500 БЕСПЛАТНЫХ ВРАЩЕНИЙ И 425% ЗА РЕГИСТРАЦИЮ НА ПЕРВЫЙ ДЕПОЗИТ ОТ 500 РУБЛЕЙ!</b> 🔥

Делай минимальный депозит
и забирай бонус от меня!

{TG_CHECK} Бонус новичкам <b>+425%</b> к депу и <b>500FS</b>
{TG_CHECK} моментальные выводы
{TG_CHECK} кешбек <b>10%</b> каждый четверг
{TG_CHECK} Турниры и розыгрыши

<b>ССЫЛКА ДЛЯ РЕГИСТРАЦИИ</b>

{TG_NEW} {TG_PURPLE_HEART}SPINTO — <a href="{SPINTO_URL}">{SPINTO_URL}</a>
{TG_NEW} {TG_PURPLE_HEART}SPINTO — <a href="{SPINTO_URL}">{SPINTO_URL}</a>
{TG_NEW} {TG_PURPLE_HEART}SPINTO — <a href="{SPINTO_URL}">{SPINTO_URL}</a>
""".strip(),
}

WELCOME_MESSAGES_BY_SOURCE = {
    SOURCE_TIKTOK: TIKTOK_WELCOME_MESSAGE,
    SOURCE_TIKTOK_NORM: TIKTOK_NORM_WELCOME_MESSAGE,
    SOURCE_YOUTUBE: YOUTUBE_WELCOME_MESSAGE,
}

INVITE_HASH_TO_SOURCE = {
    "QvKrFcrm3Ow0YjY6": SOURCE_TIKTOK,
    "Dh7BGrFXon1hZGE6": SOURCE_TIKTOK_NORM,
    "_wPQMCnnhrA1Y2Uy": SOURCE_YOUTUBE,
}

INVITE_LINK_MARKERS = {
    "+QvKrFcrm3Ow0YjY6": SOURCE_TIKTOK,
    "QvKrFcrm": SOURCE_TIKTOK,
    "+Dh7BGrFXon1hZGE6": SOURCE_TIKTOK_NORM,
    "Dh7BGrFX": SOURCE_TIKTOK_NORM,
    "+_wPQMCnnhrA1Y2Uy": SOURCE_YOUTUBE,
    "_wPQMCnn": SOURCE_YOUTUBE,
}


def normalize_invite_link(invite_link: str | None) -> str | None:
    if invite_link is None:
        return None
    return invite_link.strip().rstrip("/")


def extract_invite_hash(invite_link: str | None) -> str | None:
    normalized_link = normalize_invite_link(invite_link)
    if normalized_link is None:
        return None

    parsed = urlparse(normalized_link)
    path = parsed.path.strip("/")
    if path.startswith("+"):
        return path[1:]
    return path or None


def resolve_welcome_source(invite_link: str | None = None, invite_link_name: str | None = None) -> str | None:
    normalized_link = normalize_invite_link(invite_link)
    if normalized_link:
        for marker, source in INVITE_LINK_MARKERS.items():
            if marker in normalized_link:
                return source

    invite_hash = extract_invite_hash(invite_link)
    if invite_hash is not None:
        direct_match = INVITE_HASH_TO_SOURCE.get(invite_hash)
        if direct_match is not None:
            return direct_match

        for known_hash, source in INVITE_HASH_TO_SOURCE.items():
            if invite_hash.startswith(known_hash) or known_hash.startswith(invite_hash):
                return source

    if invite_link_name:
        name = invite_link_name.strip().lower()
        if "norm" in name:
            return SOURCE_TIKTOK_NORM
        if "tiktok" in name:
            return SOURCE_TIKTOK
        if "youtube" in name:
            return SOURCE_YOUTUBE

    return None


def get_welcome_message(source: str | None = None) -> dict:
    if source is None:
        return DEFAULT_WELCOME_MESSAGE
    return WELCOME_MESSAGES_BY_SOURCE.get(source, DEFAULT_WELCOME_MESSAGE)
