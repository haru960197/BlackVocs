class AppError(Exception):
    """Base class for domain/application errors."""

class UnauthorizedError(AppError):
    """Authentication/authorization failed."""

class TokenExpiredError(UnauthorizedError): 
    """jwt is expired"""

class InvalidTokenError(UnauthorizedError): 
    """jwt is invalid"""

class ServiceError(AppError):
    """Raised when unexpected failure in repositories or external services. This is caused by the server (not client)."""

class BadRequestError(AppError): 
    """Client sent invalid input or violated business rules."""

class ConflictError(AppError): 
    """Conflict or deplicate registration to db."""

class InvalidCredentialsError(AppError):
    """Raised when identifier or password is incorrect."""

class AuthenticationBackendError(AppError): 
    """Raised when underlying auth datastore / hashing / jwt fails."""

class NotFoundError(AppError): 
    """Raised when an item which should be in the db is not in the db."""

