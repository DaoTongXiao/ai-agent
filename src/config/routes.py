from fastapi import FastAPI
from fastapi.responses import JSONResponse

from routers.chat import router as chat_router


def register_routes(app: FastAPI):
    """
    Register all routes for the FastAPI application.

    This function includes the chat router and defines additional routes
    that were previously defined directly in main.py.
    """
    # Include the chat router with prefix and tags
    app.include_router(chat_router, prefix="/api/v1", tags=["chat"])

    # Define additional routes
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
