import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import detector
from detector import is_ai_russian


class Config:
    def __init__(self, config_path='config.json'):
        self._data = {}
        try:
            self._load(config_path)
        except:
            print("config load error, used default")
            self._data = {
                "url": "https://habr.com/ru/articles/346198/comments",
                "comment_tree_class": "tm-comments-wrapper__inner",
                "comment_text_class": "tm-comment__body-content"
            }

    def _load(self, config_path):
        path = Path(config_path)

        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(path, 'r', encoding='utf-8') as f:
            self._data = json.load(f)

    def __getitem__(self, key):
        return self._data[key]


config = Config()


def get_requester_page(url):
    response = requests.get(url)
    page = BeautifulSoup(response.text,
                         'html5lib')
    return page


def get_comments(page):
    page_title = page.find('title')
    comment_tree = BeautifulSoup(str(page.find_all('div', class_=config["comment_tree_class"])), 'html5lib')
    text_array = [x.get_text() for x in comment_tree.find_all('div', class_=config["comment_text_class"])]
    return {'Article': page_title.string, 'Comment_texts': text_array}


def dump_json(data):
    with open('output.json', 'w') as f:
        json.dump(data, f, indent=4)


def list_low_entropy(data, threshhold):
    for t in data['Comment_texts']:
        if is_ai_russian(t)<4:
            print(f'\nentropy is low, might be AI generated:')
            print(t)
    return

if __name__ == '__main__':
    web_page = get_requester_page(url=config['url'])
    comment_data = get_comments(web_page)
    list_low_entropy(comment_data,threshhold=config["ai_enthropy_threshhold"])
    dump_json(comment_data)
