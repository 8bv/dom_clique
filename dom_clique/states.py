from aiogram.dispatcher.filters.state import StatesGroup, State


class UserLoan(StatesGroup):
    wait_for_loan_amount = State()
    wait_for_percent_amount = State()
