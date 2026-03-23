import pytest
from fastapi.testclient import TestClient
import endpoint_fastapi
from main import habr_get_comments_from_url
from endpoint_fastapi import app


client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    
    assert response.status_code == 200
    assert "instruction" in response.json()
    assert response.json()["instruction"] == "input numeric habr id for array of comments"

def test_get_comments_success(monkeypatch):
    fake_result = {
        "Article": "Test",
        "Comment_texts": ["1", "2"]
    }
    
    def mock_habr_get_comments_from_url(url):
        assert url == "https://habr.com/ru/articles/12345/comments"
        return fake_result
    
    monkeypatch.setattr(endpoint_fastapi, "habr_get_comments_from_url", mock_habr_get_comments_from_url)
    
    response = client.get("/12345")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["Article"] == "Test"
    assert len(data["Comment_texts"]) == 2
    assert data["Comment_texts"][0] == "1"
    assert data["Comment_texts"][1] == "2"

def test_get_comments_empty(monkeypatch):
    fake_empty_result = {
        "Article": "Test",
        "Comment_texts": []
    }
    
    def mock_habr_get_comments_from_url(url):
        assert url == "https://habr.com/ru/articles/999/comments"
        return fake_empty_result
    
    monkeypatch.setattr(endpoint_fastapi, "habr_get_comments_from_url", mock_habr_get_comments_from_url)
    
    response = client.get("/999")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["Article"] == "Test"
    assert isinstance(data["Comment_texts"], list)
    assert len(data["Comment_texts"]) == 0