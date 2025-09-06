class AppError(Exception):
    """Base class for domain/application errors."""

class UnauthorizedError(AppError):
    """Authentication/authorization failed."""

class TokenExpiredError(UnauthorizedError): 
    "jwt is expired"

class InvalidTokenError(UnauthorizedError): 
    "jwt is invalid"

class ServiceError(AppError):
    """Unexpected failure in repositories or external services."""

class BadRequestError(AppError): 
    """Client sent invalid input or violated business rules."""

class ConflictError(AppError): 
    """Conflict or deplicate registration"""

