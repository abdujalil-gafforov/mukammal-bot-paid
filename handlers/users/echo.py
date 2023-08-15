from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.users.start import bot_start
from keyboards.default.categories import lit_ctg_btn
from keyboards.inline.download_data import see_more_btn, download_course
from loader import dp
from scrapting import get_big_categories, get_courses, course_page, check_lit_ctg
from states.main_states import CoursesListState


@dp.message_handler(lambda message: message.text == 'Ortga')
async def back(message: types.Message):
    await bot_start(message)


@dp.message_handler(lambda message: message.text in get_big_categories())
async def little_categories(message: types.Message, state: FSMContext):
    if message.text == "Ortga":
        await bot_start(message)
    else:
        order_number = get_big_categories().index(message.text)
        await state.update_data(order_number=order_number)
        if check_lit_ctg(order_number):
            await message.answer(f"{message.text} kategoriyasidagi bo'limlardan birini tanlang:",
                                 reply_markup=lit_ctg_btn(order_number))
            await CoursesListState.lit_ctg.set()


@dp.message_handler(state=CoursesListState.lit_ctg)
async def courses_list(message: types.Message, state: FSMContext):
    if message.text == "Ortga":
        await bot_start(message)
    else:
        state_data = await state.get_data()
        order_number = state_data.get('order_number')
        courses = get_courses(order_number, message.text)
        if courses:
            for i in courses:
                await message.answer_photo(i.get('photo'),
                                           f"<b>{i.get('title')}</b>\n\n"
                                           f"🕰 {i.get('duration')}\n"
                                           f"🌐 {i.get('language')}\n"
                                           f"✍ {i.get('author')}\n"
                                           f"📊 {i.get('rating')}",
                                           "HTML", reply_markup=see_more_btn(i['link']))
        else:
            await message.answer("Kechirasiz, ushbu kategoriyada hech qanday kurs mavjud emas.")
        await state.finish()
        await bot_start(message)


@dp.callback_query_handler(lambda c: c.data.startswith('see:'))
async def see_more(callback: CallbackQuery):
    course_url = 'https://coursehunter.net/course/' + callback.data[4:]
    course = course_page(course_url)
    await callback.message.answer_photo(course.get('image'),
                                        f"<b>{course.get('title')}</b>\n\n"
                                        f"📊 Rating: {course.get('rating')}\n"
                                        f"🕰 Duration: {course.get('duration')}\n"
                                        f"🌐 Language: {course.get('language')}\n"
                                        f"✍ Author: {course.get('author')}\n"
                                        f"Category: {course.get('category')}\n"
                                        f"Lessons: {course.get('lessons')}\n"
                                        f"Added Date: {course.get('added_date')}\n"
                                        f"Updated Date: {course.get('update_date')}\n"
                                        f"Release Date: {course.get('release_date')}\n"
                                        # f"More Info: <a href='{course_url}'>LINK</a>"
                                        , "HTML", reply_markup=download_course(course_url))
