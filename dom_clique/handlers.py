import logging
from decimal import Decimal
from typing import Optional

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ParseMode

from dom_clique.states import UserLoan

logger = logging.getLogger(__name__)


async def user_start(m: Message, state: FSMContext):
    logger.info("User with id: %d started", m.from_user.id)
    await m.reply(f"Привет, {m.from_user.first_name}!")
    await m.answer("Введи сумму кредита: ")
    await state.set_state(UserLoan.wait_for_loan_amount)


async def get_loan_amount(m: Message, state: FSMContext):
    amount = _try_to_get_integer(m.text)
    if amount is None:
        await m.answer("Пожлауйста, введи целое число")
        return
    elif amount < 0:
        await m.answer("Может тебе нужен вклад?")
        return

    await state.update_data(loan_amount=amount)
    await m.answer("Супер, введите сумму первоначального взноса, не менее 15% от суммы кредита")
    await state.set_state(UserLoan.wait_for_percent_amount)


async def get_percent_amount(m: Message, state: FSMContext):
    amount = _try_to_get_integer(m.text)
    if amount is None:
        await m.answer("Пожлауйста, введи целое число")
        return

    data = await state.get_data()
    loan_amount = data["loan_amount"]

    if Decimal(amount) / loan_amount < Decimal("0.15"):
        await m.answer("Сумма первоначального взноса должна быть больше 15%")
        return
    if amount > loan_amount:
        await m.answer("Сумма первоначального взноса не может быть больше суммы кредита.")
        return

    await m.answer(
        "Здорово\! А с полными условиями можно ознакомиться перейдя"
        " по [ссылке](https://www.domclick.ru/ipoteka/programs/onlajn-zayavka)",
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await state.finish()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_loan_amount, state=UserLoan.wait_for_loan_amount)
    dp.register_message_handler(get_percent_amount, state=UserLoan.wait_for_percent_amount)


def _try_to_get_integer(input_: str) -> Optional[int]:
    try:
        value = int(input_)
    except ValueError:
        return None
    return value