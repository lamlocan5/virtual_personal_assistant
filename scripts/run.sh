#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker container"
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Running locally"
    # Start the application
    uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
fi