FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home --uid 10001 bot

COPY --chown=bot:bot src ./src
COPY --chown=bot:bot sql ./sql
COPY --chown=bot:bot tiktok.jpg youtube.jpg ./

USER bot

CMD ["python", "-m", "src.main"]
