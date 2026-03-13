import json
import os
from main import dump_json


def test_json_file_created():
    data = {
        "Article": "test",
        "Comment_texts": ["1", "2"]
    }

    dump_json(data)

    assert os.path.exists("output.json")


def test_json_content_is_correct():
    data = {
        "Article": "test",
        "Comment_texts": ["1", "2"]
    }

    dump_json(data)

    with open("output.json") as file:
        saved = json.load(file)

    assert saved == data
