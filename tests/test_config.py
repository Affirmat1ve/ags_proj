import json
from pathlib import Path

from main import Config


def test_config_load(tmp_path):
    config_data = {
        "url": "http://example.com",
        "comment_tree_class": "tree",
        "comment_text_class": "text"
    }

    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data))

    config = Config(config_file)

    assert config["url"] == "http://example.com"
    assert config["comment_tree_class"] == "tree"
    assert config["comment_text_class"] == "text"

def test_missing_config():
    config = Config("missing_config.json")

    assert config["url"] == "https://habr.com/ru/articles/346198/comments"
    assert config["comment_tree_class"] == "tm-comments-wrapper__inner"
    assert config["comment_text_class"] == "tm-comment__body-content"

def test_invalid_json(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text("{invalid json}")

    config = Config(config_file)

    assert config["url"] == "https://habr.com/ru/articles/346198/comments"
    assert config["comment_tree_class"] == "tm-comments-wrapper__inner"
    assert config["comment_text_class"] == "tm-comment__body-content"
