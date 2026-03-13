from main import list_low_entropy


def test_low_entropy_comment(capsys):
    data = {
        "Article": "test",
        "Comment_texts": [
            "машина машина машина машина"
        ]
    }

    list_low_entropy(data, threshold=5)

    captured = capsys.readouterr()

    assert "entropy is low" in captured.out


def test_normal_entropy_comment(capsys):
    data = {
        "Article": "test",
        "Comment_texts": [
            "машина двигатель гараж камера"
        ]
    }

    list_low_entropy(data, threshold=0)

    captured = capsys.readouterr()

    assert captured.out == ""
