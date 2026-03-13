import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path


class Config:
    def __init__(self, config_path = 'config.json'):
        self._data = {}
        self._load(config_path)

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


if __name__ == '__main__':
    web_page = get_requester_page(url = config['url'])
    comment_data = get_comments(web_page)
    dump_json(comment_data)
