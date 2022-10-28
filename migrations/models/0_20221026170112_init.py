from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "game" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "chat_id" BIGINT NOT NULL,
    "state" SMALLINT NOT NULL,
    "start_date" TIMESTAMPTZ NOT NULL
);
COMMENT ON COLUMN "game"."state" IS 'set_in_game: 0\nday: 1\nnight: 2';
CREATE TABLE IF NOT EXISTS "game_message" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "message_id" INT NOT NULL,
    "payload" SMALLINT NOT NULL,
    "game_id" INT NOT NULL REFERENCES "game" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "game_message"."payload" IS 'set_in_game: 0\ntimer: 1';
CREATE TABLE IF NOT EXISTS "player" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "uid" BIGINT NOT NULL,
    "username" VARCHAR(150) NOT NULL,
    "role" VARCHAR(13),
    "game_id" INT NOT NULL REFERENCES "game" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "player"."role" IS 'civilian: Мирный житель\ndon: Дон\nmafia: Мафия\ncommissioner: Комиссар\ndoctor: Доктор';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
