from aiogram import Router
from aiogram.types import Message
from model.sale import Sale
from tortoise.functions import Sum

private_router = Router()

@private_router.message()
async def private_status_handler(message: Message):
    if message.chat.type == "private" and message.text == "/status":
        stats = await Sale.annotate(total=Sum("amount")).group_by("user_id").order_by("-total").all()

        temp = {}
        for sale in stats:
            temp[sale.user_id] = temp.get(sale.user_id, 0) + sale.total

        if not temp:
            await message.answer("Нет данных о продажах.")
            return
        text = "Топ продавцов по сумме всех продаж:\n"
        for sale in sorted(temp.items(), key=lambda x: x[1], reverse=True):
            text += f"{sale[0]}: {sale[1]}\n"
        await message.answer(text) 