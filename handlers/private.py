from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from model.sale import Sale
from model.admin import AdminPassword
from tortoise.functions import Sum

private_router = Router()

class ClearDBStates(StatesGroup):
    waiting_for_password = State()

class SetPasswordStates(StatesGroup):
    waiting_for_old_password = State()
    waiting_for_new_password = State()

@private_router.message()
async def private_status_handler(message: Message, state: FSMContext):
    if message.chat.type == "private" and message.text == "/start":
        await message.answer("Добро пожаловать! Весь функционал бота можно посмотреть, прописав команду /info.")
    elif message.chat.type == "private" and message.text == "/info":
        info_text = (
            "Доступные команды:\n"
            "/status — Показать топ продавцов по сумме всех продаж.\n"
            "/cleardb — Очистить базу данных продаж (требуется пароль).\n"
            "/setpassword — Сменить пароль администратора (требуется текущий пароль).\n"
            "/info — Показать это справочное сообщение.\n"
        )
        await message.answer(info_text)
    elif message.chat.type == "private" and message.text == "/status":
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
    elif message.chat.type == "private" and message.text == "/cleardb":
        await message.answer("Введите пароль для подтверждения очистки базы данных:")
        await state.set_state(ClearDBStates.waiting_for_password)
    elif message.chat.type == "private" and message.text == "/setpassword":
        await message.answer("Введите текущий пароль:")
        await state.set_state(SetPasswordStates.waiting_for_old_password)
    elif message.chat.type == "private":
        current_state = await state.get_state()
        if current_state == ClearDBStates.waiting_for_password.state:
            user_password = message.text.strip()
            db_password_obj = await AdminPassword.first()
            if not db_password_obj:
                db_password_obj = await AdminPassword.create(password="1234")
            db_password = db_password_obj.password
            if user_password == db_password:
                await Sale.all().delete()
                await message.answer("База данных продаж очищена.")
            else:
                await message.answer("Неверный пароль. Операция отменена.")
            await state.clear()
        elif current_state == SetPasswordStates.waiting_for_old_password.state:
            user_password = message.text.strip()
            db_password_obj = await AdminPassword.first()
            if not db_password_obj:
                db_password_obj = await AdminPassword.create(password="1234")
            db_password = db_password_obj.password
            if user_password == db_password:
                await message.answer("Введите новый пароль:")
                await state.set_state(SetPasswordStates.waiting_for_new_password)
            else:
                await message.answer("Неверный пароль. Операция отменена.")
                await state.clear()
        elif current_state == SetPasswordStates.waiting_for_new_password.state:
            new_password = message.text.strip()
            db_password_obj = await AdminPassword.first()
            if db_password_obj:
                db_password_obj.password = new_password
                await db_password_obj.save()
            else:
                await AdminPassword.create(password=new_password)
            await message.answer("Пароль успешно изменён.")
            await state.clear() 