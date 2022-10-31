from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "player" ALTER COLUMN "role" TYPE VARCHAR(13) USING "role"::VARCHAR(13);
        CREATE TABLE IF NOT EXISTS "vote" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "game_id" INT NOT NULL REFERENCES "game" ("id") ON DELETE CASCADE,
    "goal_user_id" BIGINT NOT NULL REFERENCES "player" ("id") ON DELETE CASCADE
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "player" ALTER COLUMN "role" TYPE VARCHAR(13) USING "role"::VARCHAR(13);
        DROP TABLE IF EXISTS "vote";"""
