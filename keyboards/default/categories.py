from aiogram.types import ReplyKeyboardMarkup

from scrapting import get_big_categories, get_little_categories
from utils.misc.little_functions import list_to_matrix

big_ctg_btn = ReplyKeyboardMarkup(list_to_matrix(get_big_categories()))


def lit_ctg_btn(order_number):
    return ReplyKeyboardMarkup(list_to_matrix(list(get_little_categories(order_number).keys()) + ['Ortga']))
