import requests
from bs4 import BeautifulSoup
import json


def get_requester_page(url):
    response = requests.get(url)
    page = BeautifulSoup(response.text,
                         'html5lib')
    return page


def get_comments(page):
    page_title = page.find('title')
    comment_tree = BeautifulSoup(str(page.find_all('div', class_='tm-comments-wrapper__inner')), 'html5lib')
    text_array = [x.get_text() for x in comment_tree.find_all('div', class_='tm-comment__body-content')]
    return {'Article': page_title.string, 'comment_texts': text_array}


def dump_json(data):
    with open('output.json', 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    url = 'https://habr.com/ru/articles/346198/comments/'
    web_page = get_requester_page(url)
    comment_data = get_comments(web_page)
    dump_json(comment_data)
