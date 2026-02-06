"""
Azure App Service Entry Point
This file is required for Azure deployment (Azure looks for app.py)
"""

from main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
