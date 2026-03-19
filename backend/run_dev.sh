#!/bin/bash
# Development server startup script

echo "Starting Chatify Python Backend..."

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the server
python -m uvicorn src.server:app --reload --port 3000 --host 0.0.0.0
