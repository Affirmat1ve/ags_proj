from main import get_requester_page, config
from bs4 import BeautifulSoup


def test_success_request_page(monkeypatch):
    class FakeResponse:
        text = "<html><title>test</title></html>"

    def fake_get(url):
        return FakeResponse()

    import requests
    monkeypatch.setattr(requests, "get", fake_get)

    page = get_requester_page("http://test.com")

    assert isinstance(page, BeautifulSoup)


def test_invalid_request_page(monkeypatch):
    def fake_get(url):
        raise Exception("network error")

    import requests
    import pytest
    monkeypatch.setattr(requests, "get", fake_get)

    with pytest.raises(Exception):
        get_requester_page("http://test.com")