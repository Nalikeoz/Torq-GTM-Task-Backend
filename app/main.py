import os
from fastapi import FastAPI
from app.routes import router

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="IP Location Service",
        description="A simple service to find country information by IP address",
        version="1.0.0"
    )
    
    app.include_router(router)
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    # Get configuration from environment variables with sensible defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
