from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "chat" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "state" SMALLINT
);
COMMENT ON COLUMN "chat"."state" IS 'set_in_game: 0';
CREATE TABLE IF NOT EXISTS "game" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "state" SMALLINT,
    "chat_id" BIGINT NOT NULL REFERENCES "chat" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "game"."state" IS 'inactive: 0\nday: 1\nnight: 2\nended: -1';
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "uid" BIGINT NOT NULL,
    "role" VARCHAR(8) NOT NULL,
    "game_id" INT NOT NULL REFERENCES "game" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "user"."role" IS 'don: Дон\nmafia: Мафия\ncommissioner: Комиссар\ndoctor: Доктор';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
