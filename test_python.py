#!/usr/bin/env python3
print("Python is working!")
print("Testing basic imports...")

try:
    import sys
    print(f"Python version: {sys.version}")
    
    import fastapi
    print("FastAPI is available")
    
    import pandas
    print("Pandas is available")
    
    import uvicorn
    print("Uvicorn is available")
    
    print("All basic dependencies are available!")
    
except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Other error: {e}")
