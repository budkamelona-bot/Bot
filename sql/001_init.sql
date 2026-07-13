CREATE TABLE IF NOT EXISTS subscribers (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE,
    chat_id BIGINT NOT NULL,
    username TEXT,
    first_name TEXT,
    subscribed_at TIMESTAMPTZ,
    is_subscription_active BOOLEAN NOT NULL DEFAULT FALSE,
    is_bot_chat_active BOOLEAN NOT NULL DEFAULT TRUE,
    welcome_source TEXT,
    welcome_sent_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE subscribers
    ADD COLUMN IF NOT EXISTS welcome_source TEXT;

CREATE INDEX IF NOT EXISTS idx_subscribers_active
    ON subscribers (is_subscription_active);
