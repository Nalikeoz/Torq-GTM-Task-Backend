"""
Error handlers for the GTM Backend API.
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.schemas.error import ErrorResponse


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions and return proper JSON error format."""
    error_response = ErrorResponse(error=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )


async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handle Starlette HTTP exceptions (like 404 Not Found)."""
    error_response = ErrorResponse(error="The requested resource was not found")
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle validation errors (e.g., invalid IP address format)."""
    error_response = ErrorResponse(error="Invalid request format. Please provide a valid IP address.")
    return JSONResponse(
        status_code=422,
        content=error_response.model_dump()
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all other unexpected exceptions."""
    error_response = ErrorResponse(error="An internal server error occurred.")
    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )

