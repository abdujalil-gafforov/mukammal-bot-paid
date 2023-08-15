from aiogram.dispatcher.filters.state import State, StatesGroup


class CoursesListState(StatesGroup):
    order_number = State()
    lit_ctg = State()
