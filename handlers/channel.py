from aiogram import Router
from aiogram.types import Message
from tortoise.transactions import in_transaction
from model.sale import Sale
import re

channel_router = Router()

SALE_PATTERN = re.compile(r"(\d+)\s+(\d+)")

@channel_router.channel_post()
async def channel_post_handler(message: Message):
    text = message.text or message.caption
    author_signature = message.author_signature
    author_id = message.sender_chat.id if message.sender_chat else None
    info = f"Новое сообщение в канале: {text}\n"
    if author_signature:
        info += f"Подпись автора: {author_signature}\n"
    if author_id:
        info += f"ID автора (sender_chat): {author_id}\n"
    else:
        info += "ID автора недоступен (Telegram не передаёт user_id обычных пользователей в каналах)\n"
    print(info)

    match = SALE_PATTERN.search(text)
    if match:
        product_id, amount = match.groups()
        amount = int(amount)
        async with in_transaction():
            await Sale.create(user_id=product_id, amount=amount, author_signature=author_signature)
        print(f"Сохранено: product_id={product_id}, amount={amount}, author_signature={author_signature}") 