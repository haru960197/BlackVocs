class AppError(Exception):
    """Base class for domain/application errors."""
#
# class UnauthorizedError(AppError):
#     """Authentication/authorization failed."""
#
# class NotFoundError(AppError):
#     """Requested resource not found."""
#
# class ConflictError(AppError):
#     """Operation conflicts with existing state."""
#
# class ServiceError(AppError):
#     """Generic internal service error."""

class BadRequestError(AppError):
    """Client sent invalid request for business rules."""
