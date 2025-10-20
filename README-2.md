# 🧠 AI Furniture Recommendation Web App

An end-to-end AI-driven web application that integrates **Machine Learning (ML)**, **Natural Language Processing (NLP)**, **Computer Vision (CV)**, and **Generative AI (GenAI)** to recommend furniture products, create dynamic product descriptions, and visualize analytics through an interactive full-stack interface.

---

## 🚀 Overview

This platform combines intelligent product recommendation with creative AI generation.  
Users can explore furniture recommendations based on **text** or **images**, view an **analytics dashboard**, and interact through a **conversational interface**.

### 🌟 Main Features

- **AI-Powered Product Recommendations** – Semantic similarity search with vector embeddings  
- **Generative Product Descriptions** – Auto-generated, creative, and detailed content  
- **Image-Based Suggestions** – Visual matching powered by computer vision models  
- **Analytics Dashboard** – Real-time insights and visualizations of product data  
- **Conversational Experience** – Chat-style recommendation interface

---

## 🧰 Tech Stack

### Backend
- **FastAPI** – Modern web framework for REST APIs  
- **FAISS** – Vector similarity search engine  
- **SentenceTransformers** – Text embedding models  
- **HuggingFace Transformers** – Generative model (FLAN-T5) for content generation  
- **PyTorch** – Deep learning backbone  

### Frontend
- **React** – Component-based UI library  
- **React Router** – Client-side navigation  
- **Axios** – API communication layer  
- **Tailwind CSS** – Utility-first styling  
- **Recharts** – Interactive data visualizations  

### AI/ML Components
- **Machine Learning** – FAISS + K-means clustering  
- **NLP** – Text embedding and semantic search  
- **Computer Vision** – Image embedding and visual similarity  
- **Generative AI** – FLAN-T5 for AI-generated descriptions  

---

## 📁 Project Structure

```
ai_recom/
├── backend/
│   ├── app.py
│   ├── working_app.py
│   ├── run_server.bat
│   └── test_endpoint.py
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Recommend.jsx
│   │   │   └── Analytics.jsx
│   │   ├── api.js
│   │   └── App.js
│   └── package.json
├── data/
│   ├── cleaned_products.csv
│   └── clustered_products.csv
├── models/
│   ├── faiss_index.bin
│   ├── image_embeddings.pkl
│   ├── kmeans.pkl
│   └── meta.pkl
└── notebooks/
    └── loadingfiles.ipynb
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd ai_recom
   ```

2. **Setup Backend**
   ```bash
   python -m venv venv
   # Activate environment
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # macOS/Linux

   pip install fastapi uvicorn pandas faiss-cpu sentence-transformers transformers torch
   ```

3. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   ```

---

## ▶️ Running the Application

1. **Start Backend**
   ```bash
   cd backend
   python app.py
   ```
   Access API at: `http://localhost:8000`

2. **Start Frontend**
   ```bash
   cd frontend
   npm start
   ```
   Visit: `http://localhost:3000`

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/` | Welcome route |
| `GET` | `/test` | Health check |
| `POST` | `/recommend` | Get product recommendations |
| `POST` | `/search-products` | Search for similar items |
| `POST` | `/recommend-by-id` | Recommend products by product ID |
| `POST` | `/generate-description` | Generate creative product description |
| `GET` | `/analytics` | View data analytics summary |

---

## 🤖 AI Modules Overview

### 1. Machine Learning
- FAISS-powered vector similarity search  
- K-Means clustering for product categorization  

### 2. Natural Language Processing
- SentenceTransformer embeddings  
- Semantic search using text vectors  

### 3. Computer Vision
- Image embeddings for visual similarity  
- Vision-based recommendations  

### 4. Generative AI
- FLAN-T5 for AI-driven content generation  
- Automatically generates engaging product descriptions  

---

## 📈 Analytics Dashboard

The dashboard provides:
- Product statistics and trends  
- Price and category insights  
- Brand and cluster analysis  
- Visualized data distributions  

---

## ⚙️ Configuration

### Environment Variables (`.env` in backend)
```env
API_HOST=0.0.0.0
API_PORT=8000
EMBEDDING_MODEL=all-MiniLM-L6-v2
GENERATION_MODEL=google/flan-t5-base
DATA_PATH=../data/cleaned_products.csv
MODEL_PATH=../models/
```

### Frontend API Configuration
`frontend/src/api.js`
```javascript
const API = axios.create({ baseURL: "http://localhost:8000" });
```

---

## 🧪 Testing

### Backend
```bash
cd backend
python test_endpoint.py
```

### Frontend
```bash
cd frontend
npm test
```

---

## 📝 Dataset Fields

- `title` — Product name  
- `brand` — Brand name  
- `description` — Product description  
- `price` — Price in local currency  
- `categories` — Product categories  
- `images` — Image URLs  
- `manufacturer` — Manufacturer name  
- `package_dimensions` — Product dimensions  
- `country_of_origin` — Origin country  
- `material` — Product material  
- `color` — Product color  
- `uniq_id` — Unique product ID  

---

## 🚀 Deployment

### Backend
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
# or production:
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
```

### Frontend
```bash
cd frontend
npm run build
```
Deploy the `build/` folder to your hosting service (e.g., Netlify, Vercel, or AWS).

---

## 🤝 Contributing

1. Fork this repository  
2. Create a new branch (`feature/your-feature`)  
3. Commit and push your changes  
4. Submit a Pull Request  

---

## 📜 License

Licensed under the **MIT License**.

---

## 🆘 Troubleshooting

### Common Issues
1. **Virtual Environment Errors**
   ```bash
   Remove-Item -Recurse -Force venv
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. **Port Already in Use**
   ```bash
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   ```
3. **Model/Data Missing**
   - Verify models are in `/models`
   - Confirm datasets in `/data`

---

## 🎯 Project Highlights

✅ ML-based product recommendation  
✅ NLP-powered semantic search  
✅ Image similarity with CV  
✅ FLAN-T5 for content generation  
✅ Full-stack app (FastAPI + React)  
✅ Analytics dashboard with Recharts  

---

## 📞 Contact

For any questions or support, please open an issue in this repository.
