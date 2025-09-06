class AppError(Exception):
    """Base class for domain/application errors."""

class UnauthorizedError(AppError):
    """Authentication/authorization failed."""

class TokenExpiredError(UnauthorizedError): 
    "jwt is expired"

class InvalidTokenError(UnauthorizedError): 
    "jwt is invalid"
