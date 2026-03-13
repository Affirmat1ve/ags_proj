import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from typing import Dict, List, Any


class Config:
    """
    Класс для загрузки и предоставления доступа к параметрам конфигурации.

    Используется для хранения URL, CSS-классов и других параметров,
    необходимых для парсинга страницы.
    """
    def __init__(self, config_path: str = 'config.json'):
        """
        Инициализирует объект Config.

        :param config_path: путь к файлу конфигурации.
        """
        self._data: Dict[str, Any] = {}
        try:
            self._load(config_path)
        except:
            print("config load error, used default")
            self._data = {
                "url": "https://habr.com/ru/articles/346198/comments",
                "comment_tree_class": "tm-comments-wrapper__inner",
                "comment_text_class": "tm-comment__body-content"
            }

    def _load(self, config_path: str):
        """
        Загружает конфигурацию из JSON-файла.

        :param config_path: путь к файлу конфигурации.
        :raises FileNotFoundError: если файл не найден.
        """
        path = Path(config_path)

        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(path, 'r', encoding='utf-8') as f:
            self._data = json.load(f)

    def __getitem__(self, key: str):
        return self._data[key]


config = Config()

def get_requester_page(url: str) -> BeautifulSoup:
    """
    Выполняет GET-запрос по указанному URL и возвращает объект BeautifulSoup.

    :param url: адрес страницы.
    :return: объект BeautifulSoup с содержимым страницы.
    """
    response = requests.get(url)
    page = BeautifulSoup(response.text,
                         'html5lib')
    return page


def get_comments(page: BeautifulSoup) -> Dict[str, Any]:
    """
    Извлекает заголовок статьи и тексты комментариев со страницы.

    :param page: объект BeautifulSoup с содержимым страницы.
    :return: словарь с ключами 'Article' и 'Comment_texts'.
    """
    page_title = page.find('title')
    comment_tree = BeautifulSoup(str(page.find_all('div', class_=config["comment_tree_class"])), 'html5lib')
    text_array = [x.get_text() for x in comment_tree.find_all('div', class_=config["comment_text_class"])]
    return {'Article': page_title.string, 'Comment_texts': text_array}


def dump_json(data: Dict[str, Any], filename: str = 'output.json'):
    """
    Сохраняет данные в JSON-файл.

    :param data: словарь с данными.
    :param filename: имя файла для сохранения.
    """
    with open('output.json', 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    web_page = get_requester_page(url = config['url'])
    comment_data = get_comments(web_page)
    dump_json(comment_data)
