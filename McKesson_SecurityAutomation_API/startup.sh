#!/bin/bash
# Startup script for Azure App Service

# Load environment variables
export $(cat .env.production | xargs)

# Start FastAPI with uvicorn
python -m uvicorn main:app --host 0.0.0.0 --port 8000
