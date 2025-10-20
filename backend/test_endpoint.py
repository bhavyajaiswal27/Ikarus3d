#!/usr/bin/env python3

import requests
import json

def test_recommend_endpoint():
    url = "http://localhost:8000/recommend"
    data = {"query": "chair", "top_k": 3}
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success! Found {len(result.get('results', []))} results")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_recommend_endpoint()


