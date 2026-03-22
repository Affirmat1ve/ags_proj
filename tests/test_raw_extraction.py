import requests

from main import extract_raw_text


def test_extract_raw_text_removes_scripts_and_styles(monkeypatch):
    html = """
    <html>
        <head>
            <script>var a = 1;</script>
            <style>body {color:red;}</style>
        </head>
        <body>
            Test
        </body>
    </html>
    """

    class FakeResponse:
        text = html

    def fake_get(url):
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    text = extract_raw_text("http://test.com")

    assert "var a = 1" not in text
    assert "color:red" not in text
    assert "Test" in text


def test_extract_raw_text_returns_clean_text(monkeypatch):
    html = """
    <html>
        <body>
            Test

            tests

            test test
        </body>
    </html>
    """

    class FakeResponse:
        text = html

    def fake_get(url):
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    text = extract_raw_text("http://test.com")

    assert isinstance(text, str)
    assert "Test" in text
    assert "tests" in text
    assert "test test" in text