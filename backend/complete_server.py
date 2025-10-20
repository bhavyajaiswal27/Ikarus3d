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

class ProductID(BaseModel):
    product_id: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Product Recommendation API"}

@app.get("/test")
def test_endpoint():
    return {"status": "working", "message": "Backend is running correctly"}

@app.post("/recommend")
def recommend_products(query: SearchQuery):
    """Handle search queries for product recommendations"""
    print(f"Received recommendation request: {query.query}")
    
    # Return mock results
    mock_results = [
        {
            "title": f"Mock Product for '{query.query}'",
            "brand": "Test Brand",
            "price": 29.99,
            "categories": "['Test', 'Category']",
            "description": f"This is a mock product result for the query: {query.query}",
            "uniq_id": "mock-id-1",
            "id": "mock-id-1"
        },
        {
            "title": f"Another Mock Product for '{query.query}'",
            "brand": "Test Brand 2", 
            "price": 39.99,
            "categories": "['Test', 'Category']",
            "description": f"Another mock result for: {query.query}",
            "uniq_id": "mock-id-2",
            "id": "mock-id-2"
        }
    ]
    
    return {"results": mock_results[:query.top_k]}

@app.post("/generate-description")
def generate_description(product: ProductID):
    """Generate creative product description"""
    print(f"Received description request for: {product.product_id}")
    
    return {
        "generated": f"This is a mock generated description for product {product.product_id}. It's a high-quality item that would be perfect for your home and lifestyle needs. Features include durable construction, modern design, and excellent value for money."
    }

@app.get("/analytics")
def get_analytics():
    """Get analytics data"""
    print("Received analytics request")
    
    return {
        "count": 100,
        "price_mean": 45.99,
        "top_categories": {
            "Home & Kitchen": 25,
            "Furniture": 20,
            "Storage": 15,
            "Bathroom": 10,
            "Office": 8
        },
        "top_brands": {
            "Test Brand": 10,
            "Sample Brand": 8,
            "Demo Brand": 5,
            "Mock Brand": 4,
            "Example Brand": 3
        },
        "cluster_stats": []
    }

if __name__ == "__main__":
    print("Starting complete server on port 8003...")
    uvicorn.run("complete_server:app", host="0.0.0.0", port=8003, reload=True)
