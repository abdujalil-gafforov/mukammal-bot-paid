from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from scrapting import get_download_links


def see_more_btn(link):
    button = InlineKeyboardButton("Batafsil ko'rish", callback_data='see:' + link.split('/')[-1])
    return InlineKeyboardMarkup().add(button)


def download_course(link):
    link1, link2 = get_download_links(link)
    buttons = InlineKeyboardMarkup(1)
    buttons.add(InlineKeyboardButton("Download course", url=link1))
    buttons.add(InlineKeyboardButton("Download course materials", url=link2))
    return buttons
