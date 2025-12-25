@echo off
REM Script to start the backend server

cd /d "E:\QUARTER-04\CLAUDE-CODE\HACKATHON-PREPARATION\DOCUSAURUS\BACKEND"

REM Activate the virtual environment
call backend_env\Scripts\activate

REM Start the FastAPI server
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

pause