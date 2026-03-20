"""
Error handling utilities for API endpoints.
"""

from fastapi import HTTPException
from typing import Any, Dict, Optional
import traceback


class AppError(Exception):
    """Base application error."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary."""
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details,
        }


class ValidationError(AppError):
    """Validation error."""

    def __init__(self, message: str, field: Optional[str] = None):
        details = {"field": field} if field else {}
        super().__init__(
            message=message,
            status_code=400,
            error_code="VALIDATION_ERROR",
            details=details,
        )


class NotFoundError(AppError):
    """Resource not found error."""

    def __init__(self, resource: str, resource_id: Optional[str] = None):
        details = {"resource": resource, "id": resource_id}
        super().__init__(
            message=f"{resource} not found",
            status_code=404,
            error_code="NOT_FOUND",
            details=details,
        )


class ServiceError(AppError):
    """Service layer error."""

    def __init__(
        self, service: str, message: str, original_error: Optional[Exception] = None
    ):
        details = {
            "service": service,
            "original_error": str(original_error) if original_error else None,
        }
        super().__init__(
            message=message,
            status_code=500,
            error_code="SERVICE_ERROR",
            details=details,
        )


def handle_error(error: Exception) -> HTTPException:
    """Convert application errors to HTTP exceptions."""
    if isinstance(error, AppError):
        return HTTPException(
            status_code=error.status_code,
            detail=error.to_dict(),
        )

    # Log unexpected errors
    print(f"Unexpected error: {error}")
    traceback.print_exc()

    return HTTPException(
        status_code=500,
        detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred",
            "details": {"type": type(error).__name__},
        },
    )


def safe_execute(func):
    """Decorator for safe execution with error handling."""

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AppError as e:
            raise handle_error(e)
        except Exception as e:
            raise handle_error(e)

    return wrapper
