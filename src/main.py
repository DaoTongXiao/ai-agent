from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="AI Agent API", version="0.1.0")


@app.get("/", summary="Health check", tags=["system"])
def read_root():
    """
    Simple health check endpoint.
    """
    return {"status": "ok", "message": "Service is running"}


@app.get("/hello", summary="Greet a user", tags=["demo"])
def say_hello(name: str = "world"):
    """
    A simple demo endpoint that returns a greeting.

    Query Parameters:
    - name: Optional name to include in the greeting.
    """
    return {"message": f"Hello, {name}!"}


@app.get("/ping", summary="Ping endpoint", tags=["system"])
def ping():
    """
    Lightweight ping endpoint for quick checks.
    """
    return JSONResponse(content={"ping": "pong"})


if __name__ == "__main__":
    # Run with: python -m uvicorn src.main:app --reload
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
