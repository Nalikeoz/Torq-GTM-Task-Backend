import uvicorn
from fastapi import FastAPI, HTTPException
from app.core.config import settings
from app.api.v1.routes.ip2location import router
from app.core.error_handlers import (
    http_exception_handler,
    starlette_http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.title,
        description=settings.description,
        version=settings.version
    )
    
    # Include API routers
    app.include_router(router)
    
    # Register exception handlers
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, starlette_http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    return app

app = create_app()

if __name__ == "__main__":
    print(f"Starting server on {settings.host}:{settings.port}")
    uvicorn.run(app, host=settings.host, port=settings.port)
