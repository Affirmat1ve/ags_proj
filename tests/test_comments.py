from main import get_requester_page, get_comments, config
from bs4 import BeautifulSoup


def test_page_with_comments_and_title():
    page = get_requester_page(config["url"])
    result = get_comments(page)

    assert "Article" in result
    assert "Comment_texts" in result
    assert isinstance(result["Comment_texts"], list)


def test_page_without_comments():
    html = """
    <html>
        <title>test</title>
    </html>
    """

    page = BeautifulSoup(html, "html5lib")

    result = get_comments(page)

    assert result["Article"] == "test"
    assert result["Comment_texts"] == []


def test_page_without_title():
    import pytest

    html = """
    <html>
        <body>
            <div class="tm-comments-wrapper__inner">
                <div class="tm-comment__body-content">test comment</div>
            </div>
        </body>
    </html>
    """

    page = BeautifulSoup(html, "html5lib")

    with pytest.raises(AttributeError):
        get_comments(page)
