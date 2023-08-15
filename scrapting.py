from bs4 import BeautifulSoup
import requests

pageResponse = requests.get("https://coursehunter.net/").text
soup = BeautifulSoup(pageResponse, "html.parser")


def get_big_categories() -> list[str]:
    return [i.a['title'] for i in soup.li.ul.contents[1::2]]

# def get_ctg


def check_lit_ctg(order_number: int) -> bool:
    return bool(soup.li.ul.contents[1::2][order_number].ul)


def get_little_categories(order_number: int) -> dict or list:
    return {i.a.get('title'): i.a.get('href') for i in
            soup.li.ul.contents[1::2][order_number].ul.contents[1::2]}


def get_courses(order_number: int, lit_category_name: str) -> list[dict]:
    page = requests.get(
        get_little_categories(order_number).get(
            lit_category_name) + '?sort=created_at&order=desc&price%5B%5D=free').text
    soup = BeautifulSoup(page, "html.parser")
    return [{
        'photo': 'https:' + i.img.get('srcset')[:-3],
        'title': i.h3.text,
        'link': i.find('a', class_='btn').get('href'),
        'duration': i.find(class_="course-duration").text.strip(),
        'language': i.find(class_="course-lang").text.strip(),
        'author': " ".join(i.find(class_="course-lessons").text.strip().split()),
        'rating': i.find(class_="course-rating-on").get('data-text')

    } for i in
        soup.find('div', class_="main--row main--row_reverse").div.div.contents[1::2]]


def course_page(url):
    sp = BeautifulSoup(requests.get(url).text, "html.parser")
    data = sp.find_all(class_="course-box-value")
    return {
        "image": 'https:' + sp.find('img').get('src'),
        "title": sp.find(class_="raw-title").text,
        "rating": sp.find(class_="raw-rating-on").get('data-text'),
        "duration": data[0].text,
        "author": ", ".join([i.text for i in data[1:-6]]),
        "category": data[-6].text,
        "lessons": data[-5].text,
        "added_date": data[-4].text,
        "language": data[-3].text,
        "release_date": data[-2].text,
        "update_date": data[-1].text,
        # 'description': sp.find(class_="book-wrap-description").text  # .prettify()
    }


def get_download_links(url):
    sp = BeautifulSoup(requests.get(url).text, "html.parser")
    return (i.get('href') for i in sp.find_all(class_="book-wrap-btn"))
