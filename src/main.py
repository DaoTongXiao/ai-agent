import uvicorn
from fastapi import FastAPI

from config.routes import register_routes

app = FastAPI(title="AI Agent API", version="0.1.0")

register_routes(app)


if __name__ == "__main__":
    # Run with: python -m uvicorn src.main:app --reload
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
