import uvicorn
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.routes.ip2location import router

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.title,
        description=settings.description,
        version=settings.version
    )
    
    # Include API routers
    app.include_router(router)
    
    return app

app = create_app()

if __name__ == "__main__":
    print(f"Starting server on {settings.host}:{settings.port}")
    uvicorn.run(app, host=settings.host, port=settings.port)
