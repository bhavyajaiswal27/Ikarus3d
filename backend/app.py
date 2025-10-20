from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import faiss
import pickle
import os
import traceback
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
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
    
    # Text generation model
    tok = AutoTokenizer.from_pretrained("google/flan-t5-base")
    gen_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base").to(
        "cuda" if torch.cuda.is_available() else "cpu"
    )
    
    # Load clustered data
    clustered_df = pd.read_csv("data/clustered_products.csv")
    
    # Add id column to clustered data if it doesn't exist
    if 'id' not in clustered_df.columns:
        clustered_df['id'] = clustered_df['uniq_id']
    
    print("All models and data loaded successfully!")
except Exception as e:
    print(f"Error loading models or data: {e}")
    raise

# Define request models
class SearchQuery(BaseModel):
    query: str
    top_k: int = 5

class ProductID(BaseModel):
    product_id: str

# Add a simple test endpoint to verify the server is working
@app.get("/test")
def test_endpoint():
    return {"status": "working", "message": "Backend is running correctly"}

# Define API endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Product Recommendation API"}


@app.post("/search-products")
def search_products(query: SearchQuery):
    """Handle search queries for product recommendations"""
    try:
        print(f"Search query: {query.query}, top_k: {query.top_k}")
        
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
        traceback.print_exc()  # Print full traceback for debugging
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend")
def recommend_products(query: SearchQuery):
    """Handle search queries for product recommendations - same as search-products"""
    try:
        print(f"Received request - Search query: {query.query}, top_k: {query.top_k}")
        print(f"Query type: {type(query)}, Query object: {query}")
        
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
        traceback.print_exc()  # Print full traceback for debugging
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend-by-id")
def recommend_by_product_id(product: ProductID):
    """Recommend similar products based on a product ID"""
    try:
        print(f"Recommend for product_id: {product.product_id}")
        
        # Find product in dataframe
        product_row = df[df["id"] == product.product_id]
        
        if product_row.empty:
            # Try with uniq_id if id doesn't match
            product_row = df[df["uniq_id"] == product.product_id]
            if product_row.empty:
                raise HTTPException(status_code=404, detail="Product not found")
            # Use uniq_id as id for lookup
            product_id = product.product_id
        else:
            product_id = product.product_id
        
        # Get product index in meta
        try:
            product_idx = meta["ids"].index(product_id)
            
            # Get product embedding
            product_embedding = index.reconstruct(product_idx)
            
            # Search similar products
            D, I = index.search(product_embedding.reshape(1, -1), 6)  # Get 6 to exclude the product itself
            
            # Remove the query product (should be the first result)
            if I[0][0] == product_idx:
                I = I[0][1:]
            else:
                I = I[0][:5]
            
            # Get product IDs
            product_ids = [meta["ids"][i] for i in I]
            
            # Get product details
            results = df[df["id"].isin(product_ids)].to_dict(orient="records")
            
            # Ensure id field exists in results
            for result in results:
                if "id" not in result and "uniq_id" in result:
                    result["id"] = result["uniq_id"]
            
            return {"results": results}
        except ValueError as e:
            print(f"Error finding product index: {str(e)}")
            # If product not in meta, return empty results
            return {"results": []}
    except Exception as e:
        print(f"Error in recommend_by_product_id: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-description")
def generate_description(product: ProductID):
    """Generate creative product description using GenAI"""
    try:
        print(f"Generating description for product_id: {product.product_id}")
        
        # Find product in dataframe
        product_row = df[df["id"] == product.product_id]
        
        if product_row.empty:
            # Try with uniq_id if id doesn't match
            product_row = df[df["uniq_id"] == product.product_id]
            if product_row.empty:
                raise HTTPException(status_code=404, detail="Product not found")
        
        # Get product details
        product_data = product_row.iloc[0]
        title = product_data.get('title', '')
        brand = product_data.get('brand', '')
        category = product_data.get('categories', '')
        material = product_data.get('material', '')
        color = product_data.get('color', '')
        
        # Create prompt for description generation
        prompt = f"Generate a creative and engaging product description for: {title} by {brand}. Category: {category}. Material: {material}. Color: {color}. Make it appealing and highlight key features."
        
        # Generate description using the model
        inputs = tok(prompt, return_tensors="pt", max_length=512, truncation=True)
        
        with torch.no_grad():
            outputs = gen_model.generate(
                inputs.input_ids,
                max_length=150,
                num_beams=4,
                early_stopping=True,
                temperature=0.7
            )
        
        generated_text = tok.decode(outputs[0], skip_special_tokens=True)
        
        return {"generated": generated_text}
        
    except Exception as e:
        print(f"Error in generate_description: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
def get_analytics():
    try:
        print("Getting analytics data")
        
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
        
        # Cluster statistics (if available)
        cluster_stats = []
        if 'cluster' in clustered_df.columns:
            try:
                cluster_stats = clustered_df.groupby("cluster").agg({
                    "id": "count",
                    "price": ["mean", "min", "max"] if 'price' in clustered_df.columns else "count"
                }).reset_index()
                
                # Flatten column names
                cluster_stats.columns = ["cluster", "count", "avg_price", "min_price", "max_price"]
                cluster_stats = cluster_stats.to_dict(orient="records")
            except Exception as e:
                print(f"Error processing cluster stats: {e}")
                cluster_stats = []
        
        return {
            "count": total_count,
            "price_mean": price_mean,
            "top_categories": top_categories,
            "top_brands": top_brands,
            "cluster_stats": cluster_stats
        }
    except Exception as e:
        print(f"Error in get_analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Run the app
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)