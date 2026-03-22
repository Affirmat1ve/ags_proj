import json
import os
import pytest
from bs4 import BeautifulSoup

from main import Config, dump_json, extract_raw_text, habr_get_comments_from_url, list_low_entropy


def test_full_pipeline(monkeypatch, tmp_path):
    html = """
    <html>
        <title>Test article</title>
        <div class="tm-comments-wrapper__inner">
            <div class="tm-comment__body-content">comment 1</div>
            <div class="tm-comment__body-content">comment 2</div>
        </div>
    </html>
    """

    class FakeResponse:
        text = html

    def fake_get(url):
        return FakeResponse()

    import requests
    monkeypatch.setattr(requests, "get", fake_get)

    monkeypatch.chdir(tmp_path)

    result = habr_get_comments_from_url("http://test.com")
    dump_json(result)

    assert result["Article"] == "Test article"
    assert len(result["Comment_texts"]) == 2
    assert os.path.exists("output.json")

def test_pipeline_with_entropy_check(monkeypatch, capsys):
    html = """
    <html>
        <title>Test article</title>
        <div class="tm-comments-wrapper__inner">
            <div class="tm-comment__body-content">AI text</div>
        </div>
    </html>
    """

    class FakeResponse:
        text = html

    def fake_get(url):
        return FakeResponse()

    def fake_entropy(text):
        return 0.5

    import requests
    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr("main.is_ai_russian", fake_entropy)

    data = habr_get_comments_from_url("http://test.com")
    list_low_entropy(data, threshold=4)

    captured = capsys.readouterr()
    assert "entropy is low" in captured.out

def test_pipeline_with_custom_config(monkeypatch, tmp_path):
    config_data = {
        "url": "http://test.com",
        "comment_tree_class": "tm-comments-wrapper__inner",
        "comment_text_class": "tm-comment__body-content",
        "ai_enthropy_threshold": 4
    }

    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data))

    config = Config(config_file)

    html = """
    <html>
        <title>Config test</title>
        <div class="tm-comments-wrapper__inner">
            <div class="tm-comment__body-content">comment</div>
        </div>
    </html>
    """

    class FakeResponse:
        text = html

    def fake_get(url):
        return FakeResponse()

    import requests
    monkeypatch.setattr(requests, "get", fake_get)

    result = habr_get_comments_from_url(config["url"])

    assert result["Article"] == "Config test"
    assert result["Comment_texts"] == ["comment"]

def test_extract_raw_text_integration(monkeypatch):
    html = """
    <html>
        <script>var a = 1</script>
        <style>body {color:red}</style>
        <body>
            Test
            test text
        </body>
    </html>
    """

    class FakeResponse:
        text = html

    def fake_get(url):
        return FakeResponse()

    import requests
    monkeypatch.setattr(requests, "get", fake_get)

    text = extract_raw_text("http://test.com")

    assert "var a = 1" not in text
    assert "color:red" not in text
    assert "Test" in text