"""
Centralized Exception Hierarchy
=================================

WHY do we need custom exceptions?
  In a real project, different layers throw different errors:
  - A repository might find "record not found"
  - A service might say "business rule violated"
  - An engine might say "optimization infeasible"

  If every layer just raises generic `Exception`, the API layer
  has no way to know WHAT went wrong or WHAT HTTP status to return.

  Custom exceptions solve this:
  - Each exception carries a meaningful message + error code
  - The API layer catches them and maps to proper HTTP responses
  - Future phases will add a global exception handler in main.py
    that automatically converts these to JSON error responses

HOW TO USE (for future phases):
  1. Define domain-specific exceptions by inheriting from AppException.
  2. Raise them in services/repositories.
  3. The global handler (added later) catches and returns proper HTTP errors.

EXAMPLE:
  class BlockConflictError(AppException):
      def __init__(self, block_id: int):
          super().__init__(
              message=f"Block {block_id} conflicts with existing schedule",
              error_code="BLOCK_CONFLICT",
              status_code=409,
          )
"""


class AppException(Exception):
    """
    Base exception for all application-specific errors.

    Every custom exception in this project should inherit from this class.
    This lets the global exception handler catch ALL app errors in one place.

    Attributes:
        message:     Human-readable description of what went wrong.
        error_code:  Machine-readable code (e.g., "NOT_FOUND", "CONFLICT").
                     Frontend can use this to show the right error message.
        status_code: HTTP status code to return (e.g., 404, 409, 422).
    """

    def __init__(
        self,
        message: str = "An unexpected error occurred",
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)


# ── 404 — Resource Not Found ─────────────────────────────────


class NotFoundException(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str = "Resource", resource_id: str | int = ""):
        detail = f"{resource} not found"
        if resource_id:
            detail = f"{resource} with id '{resource_id}' not found"
        super().__init__(
            message=detail,
            error_code="NOT_FOUND",
            status_code=404,
        )


# ── 409 — Conflict ───────────────────────────────────────────


class ConflictException(AppException):
    """Raised when an action conflicts with existing state (e.g., duplicate entry)."""

    def __init__(self, message: str = "Resource conflict"):
        super().__init__(
            message=message,
            error_code="CONFLICT",
            status_code=409,
        )


# ── 422 — Validation / Business Rule Violation ───────────────


class ValidationException(AppException):
    """Raised when input passes schema validation but violates a business rule."""

    def __init__(self, message: str = "Validation error"):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=422,
        )


# ── 503 — Service Unavailable ────────────────────────────────


class ServiceUnavailableException(AppException):
    """Raised when an external dependency (DB, Redis, etc.) is not reachable."""

    def __init__(self, service: str = "External service"):
        super().__init__(
            message=f"{service} is currently unavailable",
            error_code="SERVICE_UNAVAILABLE",
            status_code=503,
        )
