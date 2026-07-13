# Telegram Channel Subscription Bot (Python)

Python-версия Telegram-бота для канала.

## Что делает бот

- при подтверждении подписки отправляет одно welcome-сообщение
- защищается от дублей
- помнит блокировку бота пользователем

## Рекомендуемый Telegram-сценарий

Лучший вариант — включить в канале join requests и сделать бота администратором.
Тогда бот сможет:

1. получить `chat_join_request`
2. одобрить заявку
3. записать пользователя в БД
4. отправить welcome-сообщение в личку

Fallback-сценарий тоже есть:

- пользователь открывает бота и пишет `/start`
- бот проверяет подписку на канал
- пользователь может отправить `/check`

## Стек

- Python 3.11+
- aiogram
- asyncpg
- PostgreSQL

## Структура проекта

```text
telegram-channel-bot-python/
├─ .env.example
├─ requirements.txt
├─ README.md
├─ sql/
│  └─ 001_init.sql
└─ src/
   ├─ main.py
   ├─ bot_factory.py
   ├─ config/
   │  ├─ settings.py
   │  └─ messages.py
   ├─ db/
   │  └─ pool.py
   ├─ handlers/
   │  ├─ start_handler.py
   │  ├─ check_handler.py
   │  ├─ chat_join_request_handler.py
   │  ├─ chat_member_handler.py
   │  └─ my_chat_member_handler.py
   ├─ repositories/
   │  └─ subscriber_repository.py
   ├─ services/
   │  ├─ messaging_service.py
   │  ├─ subscription_service.py
   ├─ types/
   │  └─ subscriber.py
   └─ utils/
      ├─ logger.py
      └─ telegram_utils.py
```

## Настройка

### 1. Создайте и заполните `.env`

```bash
cp .env.example .env
```

### 2. Создайте виртуальное окружение и установите зависимости

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Создайте БД и примените SQL

```bash
createdb telegram_bot
psql "$DATABASE_URL" -f sql/001_init.sql
```

### 4. Запустите бота

```bash
python -m src.main
```

## Деплой на Railway

Проект готов к запуску как постоянный worker-процесс:

- Railway автоматически использует корневой `Dockerfile`
- `railway.json` задаёт команду запуска и перезапуск после сбоя
- при старте бот ждёт PostgreSQL и сам применяет `sql/001_init.sql`
- публичный домен и HTTP-порт этому боту не нужны

### 1. Отправьте проект в GitHub

Не добавляйте локальный `.env` в репозиторий. Все секреты задаются в Railway.

```bash
git add .
git commit -m "Prepare bot for Railway deployment"
git push
```

### 2. Создайте проект и PostgreSQL

1. В Railway нажмите **New Project** и создайте пустой проект.
2. Нажмите **+ New** → **Database** → **PostgreSQL**.
3. Дождитесь статуса `Online` у PostgreSQL.

### 3. Подключите бота

1. Нажмите **+ New** → **GitHub Repo**.
2. Выберите репозиторий с ботом и нужную ветку.
3. Railway обнаружит `Dockerfile` в корне автоматически.

### 4. Добавьте переменные

Откройте сервис бота → **Variables** и добавьте:

```dotenv
BOT_TOKEN=токен_из_BotFather
DATABASE_URL=${{Postgres.DATABASE_URL}}
CHANNEL_ID=-1001234567890
CHANNEL_LINK=https://t.me/ссылка_на_канал
LOG_LEVEL=INFO
```

Если сервис базы называется не `Postgres`, выберите её `DATABASE_URL` через меню автодополнения Railway. `TELEGRAM_PROXY_URL` на Railway добавлять не нужно, если Telegram доступен напрямую.

### 5. Запустите и проверьте

1. Нажмите **Deploy** для применения переменных.
2. В **Deployments** → **View Logs** дождитесь строк `Bot started successfully` и `Start polling`.
3. Проверьте обе пригласительные ссылки Telegram.

Для бота должен работать ровно один экземпляр сервиса. Не включайте Serverless и не создавайте публичный домен: polling-процесс должен быть запущен постоянно.

## Важные настройки Telegram

- бот должен быть администратором канала
- для join requests у бота должно быть право одобрять заявки
- бот должен получать `chat_member` и `chat_join_request`
- если пользователь никогда не писал боту, обычная подписка без join requests может не позволить отправить ему личное сообщение
- если сеть не открывает `https://api.telegram.org`, можно задать `TELEGRAM_PROXY_URL`, например `socks5://127.0.0.1:1080`

## Где задаются тексты

Файл:

- `src/config/messages.py`

Там находятся:

- `WELCOME_MESSAGE` — единственное приветственное сообщение

## Антидубли

Используются поля:

- `welcome_sent_at`
