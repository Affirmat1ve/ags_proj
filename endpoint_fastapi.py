from fastapi import FastAPI
from main import habr_get_comments_from_url


app = FastAPI()

@app.get("/")
async def root():
    return {"instruction": "input numeric habr id for array of comments"}

@app.get("/{habr_id}")
async def read_item(habr_id: str):
    url = f"https://habr.com/ru/articles/{habr_id}/comments"
    result = habr_get_comments_from_url(url)
    return result