@echo off

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if running in Docker
if exist /.dockerenv (
    echo Running in Docker container
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
) else (
    echo Running locally
    REM Start the application
    uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
)
pause