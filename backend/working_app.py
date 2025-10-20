from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import faiss
import pickle
import os
import traceback
from sentence_transformers import SentenceTransformer
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

# Set working directory to project root
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("Current working directory:", os.getcwd())

# Load data and models
try:
    # Load product dataset
    df = pd.read_csv("data/cleaned_products.csv")
    
    # Add id column if it doesn't exist (use uniq_id as id)
    if 'id' not in df.columns:
        df['id'] = df['uniq_id']
    
    # Load FAISS index
    index = faiss.read_index("models/faiss_index.bin")
    
    # Load metadata
    with open("models/meta.pkl", "rb") as f:
        meta = pickle.load(f)
    
    # Embedding model
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    
    print("All models and data loaded successfully!")
except Exception as e:
    print(f"Error loading models or data: {e}")
    # Set up mock data for testing
    df = None
    index = None
    meta = None
    embed_model = None

# Define request models
class SearchQuery(BaseModel):
    query: str
    top_k: int = 5

class ProductID(BaseModel):
    product_id: str

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
        
        # If models are not loaded, return mock data
        if df is None or index is None or meta is None or embed_model is None:
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
        
        # Encode query
        query_embedding = embed_model.encode([query.query])[0]
        
        # Search in FAISS index
        D, I = index.search(query_embedding.reshape(1, -1), query.top_k)
        
        # Get product IDs
        product_ids = [meta["ids"][i] for i in I[0]]
        print(f"Found product IDs: {product_ids}")
        
        # Get product details - use both id and uniq_id for compatibility
        id_results = df[df["id"].isin(product_ids)]
        uniq_id_results = df[df["uniq_id"].isin(product_ids)]
        results = pd.concat([id_results, uniq_id_results]).drop_duplicates().to_dict(orient="records")
        
        # Ensure id field exists in results
        for result in results:
            if "id" not in result and "uniq_id" in result:
                result["id"] = result["uniq_id"]
            elif "uniq_id" not in result and "id" in result:
                result["uniq_id"] = result["id"]
        
        print(f"Returning {len(results)} results")
        return {"results": results}
        
    except Exception as e:
        print(f"Error in recommend_products: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
def get_analytics():
    try:
        print("Getting analytics data")
        
        if df is None:
            return {
                "count": 0,
                "price_mean": 0,
                "top_categories": {},
                "top_brands": {},
                "cluster_stats": []
            }
        
        # Basic statistics
        total_count = len(df)
        price_mean = df['price'].mean() if 'price' in df.columns else 0
        
        # Top categories
        if 'categories' in df.columns:
            # Parse categories (they're stored as strings like "['Home & Kitchen', 'Furniture']")
            all_categories = []
            for cat_str in df['categories'].dropna():
                try:
                    # Remove brackets and quotes, then split
                    cat_str = cat_str.strip("[]'\"")
                    categories = [c.strip().strip("'\"") for c in cat_str.split(',')]
                    all_categories.extend(categories)
                except:
                    continue
            
            from collections import Counter
            top_categories = dict(Counter(all_categories).most_common(10))
        else:
            top_categories = {}
        
        # Top brands
        if 'brand' in df.columns:
            from collections import Counter
            top_brands = dict(Counter(df['brand'].dropna()).most_common(10))
        else:
            top_brands = {}
        
        return {
            "count": total_count,
            "price_mean": price_mean,
            "top_categories": top_categories,
            "top_brands": top_brands,
            "cluster_stats": []
        }
    except Exception as e:
        print(f"Error in get_analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run("working_app:app", host="0.0.0.0", port=8000, reload=True)

