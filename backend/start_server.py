#!/usr/bin/env python3

import uvicorn
import os
import sys

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Change to the project root directory (one level up from backend)
project_root = os.path.dirname(backend_dir)
os.chdir(project_root)

print(f"Starting server from: {os.getcwd()}")
print(f"Backend directory: {backend_dir}")

if __name__ == "__main__":
    try:
        uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()

