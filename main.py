import requests # импортируем библиотеку удаленных запросов
from bs4 import BeautifulSoup # импортируем библиотеку парсинга BeautifulSoup
import json




def get_comments(url):
    response = requests.get(url)  # выполняем запрос к удаленному серверу Timeweb Cloud
    page = BeautifulSoup(response.text, 'html5lib')  # парсим ответ удаленного сервера, указывая в качестве процессора парсера библиотеку html5lib
    pageTitle = page.find('title')
    comment_tree = BeautifulSoup(str(page.find_all('div', class_='tm-comments-wrapper__inner')), 'html5lib')
    text_array = [x.get_text() for x in comment_tree.find_all('div', class_='tm-comment__body-content')]
    return {'Article': pageTitle.string, 'comment_texts': text_array}

def dump_json(data):
    with open('output.json', 'w') as f:
        json.dump(data, f, indent=4)  # Writes pretty-printed JSON to file


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = 'https://habr.com/ru/articles/346198/comments/'
    get_comments(url)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
