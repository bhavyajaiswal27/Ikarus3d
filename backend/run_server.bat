@echo off
cd /d %~dp0
cd ..
cd backend
..\venv\Scripts\python.exe -m uvicorn app:app --host 0.0.0.0 --port 8000