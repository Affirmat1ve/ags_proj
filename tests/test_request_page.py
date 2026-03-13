from main import get_requester_page, config
from bs4 import BeautifulSoup


def test_success_request_page():
    page = get_requester_page(config["url"])

    assert isinstance(page, BeautifulSoup)


def test_invalid_request_page():
    import pytest

    with pytest.raises(Exception):
        get_requester_page("http://invalid-url.com")
