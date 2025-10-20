from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchQuery(BaseModel):
    query: str
    top_k: int = 5

class ProductID(BaseModel):
    product_id: str

@app.get("/")
def root():
    return {"message": "Server is working!"}

@app.get("/test")
def test():
    return {"status": "ok", "message": "Test endpoint working"}

@app.post("/recommend")
def recommend(query: SearchQuery):
    return {
        "results": [
            {
                "title": f"Test product for: {query.query}",
                "brand": "Test Brand",
                "price": 25.99,
                "categories": "['Test']",
                "description": f"This is a test result for {query.query}",
                "uniq_id": "test-1",
                "id": "test-1"
            }
        ]
    }

@app.post("/generate-description")
def generate_description(product: ProductID):
    """Generate creative product description"""
    return {
        "generated": f"This is a mock generated description for product {product.product_id}. It's a high-quality item that would be perfect for your home and lifestyle needs."
    }

@app.get("/analytics")
def get_analytics():
    """Get analytics data"""
    return {
        "count": 100,
        "price_mean": 45.99,
        "top_categories": {
            "Home & Kitchen": 25,
            "Furniture": 20,
            "Storage": 15
        },
        "top_brands": {
            "Test Brand": 10,
            "Sample Brand": 8,
            "Demo Brand": 5
        },
        "cluster_stats": []
    }

if __name__ == "__main__":
    print("Starting basic server on port 8002...")
    uvicorn.run(app, host="0.0.0.0", port=8002)
