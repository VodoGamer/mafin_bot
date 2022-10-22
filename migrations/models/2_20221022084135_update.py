from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "player" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "uid" BIGINT NOT NULL,
    "role" VARCHAR(13),
    "game_id" INT NOT NULL REFERENCES "game" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "player"."role" IS 'civilian: Мирный житель\ndon: Дон\nmafia: Мафия\ncommissioner: Комиссар\ndoctor: Доктор';;
        DROP TABLE IF EXISTS "user";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "player";"""
