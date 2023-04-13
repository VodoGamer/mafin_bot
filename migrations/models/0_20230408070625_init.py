from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "chat" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "game" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "state" VARCHAR(18) NOT NULL,
    "chat_id" BIGINT NOT NULL REFERENCES "chat" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "game"."state" IS 'enrollment: enrollment in game';
CREATE TABLE IF NOT EXISTS "game_message" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "message_id" INT NOT NULL,
    "payload" VARCHAR(26) NOT NULL,
    "game_id" INT NOT NULL REFERENCES "game" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "game_message"."payload" IS 'enrollment: enrollment in game message';
CREATE TABLE IF NOT EXISTS "player" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "game_id" INT NOT NULL REFERENCES "game" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
