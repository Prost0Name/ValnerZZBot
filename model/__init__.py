from tortoise import Tortoise
from config import DATABASE_URL

async def init_db():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={"models": ["model.sale", "model.admin"]}
    )
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()
