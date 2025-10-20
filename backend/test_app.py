from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SearchQuery(BaseModel):
    query: str
    top_k: int = 5

@app.get("/")
def read_root():
    return {"message": "Test API"}

@app.post("/test-recommend")
def test_recommend(query: SearchQuery):
    return {"message": f"Received query: {query.query}, top_k: {query.top_k}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test_app:app", host="0.0.0.0", port=8001, reload=True)


