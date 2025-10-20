from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="AI Product Recommendation API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request models
class SearchQuery(BaseModel):
    query: str
    top_k: int = 5

# Test endpoint
@app.get("/test")
def test_endpoint():
    return {"status": "working", "message": "Backend is running correctly"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Product Recommendation API"}

@app.post("/recommend")
def recommend_products(query: SearchQuery):
    """Handle search queries for product recommendations"""
    try:
        print(f"Received request - Search query: {query.query}, top_k: {query.top_k}")
        
        # For now, return mock data to test the endpoint
        mock_results = [
            {
                "title": f"Mock Product for '{query.query}'",
                "brand": "Test Brand",
                "price": 29.99,
                "categories": "['Test', 'Category']",
                "description": f"This is a mock product result for the query: {query.query}",
                "uniq_id": "mock-id-1"
            },
            {
                "title": f"Another Mock Product for '{query.query}'",
                "brand": "Test Brand 2", 
                "price": 39.99,
                "categories": "['Test', 'Category']",
                "description": f"Another mock result for: {query.query}",
                "uniq_id": "mock-id-2"
            }
        ]
        
        return {"results": mock_results[:query.top_k]}
        
    except Exception as e:
        print(f"Error in recommend_products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("simple_app:app", host="127.0.0.1", port=8001, reload=True)
