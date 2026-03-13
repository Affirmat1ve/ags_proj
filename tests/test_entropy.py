from detector import russian_entropy


def test_entropy_empty_text():
    result = russian_entropy("")
    assert result == 0


def test_entropy_single_word():
    result = russian_entropy("машина")
    assert result == 0


def test_entropy_multiple_words():
    result = russian_entropy("машина мотор двигатель")
    assert result > 0
