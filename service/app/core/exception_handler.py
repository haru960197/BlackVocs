from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse

from fastapi.exceptions import RequestValidationError
from pymongo import errors as mongo_errors
from core.errors import (
    UnauthorizedError, TokenExpiredError, InvalidTokenError,
    BadRequestError, ConflictError, ServiceError, 
    InvalidCredentialsError, AuthenticationBackendError
)

def register_exception_handlers(app):
    # --- Domain errors -> HTTP ---
    @app.exception_handler(UnauthorizedError)
    async def unauthorized_handler(request: Request, exc: UnauthorizedError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": {"type": exc.__class__.__name__, "detail": str(exc) or "Unauthorized"}},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(TokenExpiredError)
    async def token_expired_handler(request: Request, exc: TokenExpiredError):
        return await unauthorized_handler(request, exc)

    @app.exception_handler(InvalidTokenError)
    async def invalid_token_handler(request: Request, exc: InvalidTokenError):
        return await unauthorized_handler(request, exc)

    @app.exception_handler(BadRequestError)
    async def bad_request_handler(request: Request, exc: BadRequestError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": {"type": "BadRequest", "detail": str(exc) or "Bad request"}},
        )

    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: ConflictError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": {"type": "Conflict", "detail": str(exc) or "Conflict"}},
        )

    @app.exception_handler(ServiceError)
    async def service_error_handler(request: Request, exc: ServiceError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": {"type": "ServiceError", "detail": str(exc) or "Internal server error"}},
        )

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": {"type": "Invalid Credential Error", "detail": str(exc) or "credenals are invalid"}},
        )

    @app.exception_handler(AuthenticationBackendError)
    async def auth_backend_error_handler(request: Request, exc: AuthenticationBackendError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": {"type": "Authentication backend failure", "detail": str(exc) or "Authentication backend failure"}},
        )
    # ---------- Framework-level ----------
    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        # Pydantic/validation errors for request bodies/query params -> 422
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": {"type": "ValidationError", "detail": exc.errors()}},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"type": "HTTPException", "detail": exc.detail}},
            headers=getattr(exc, "headers", None),
        )

    # ---------- Mongo-specific (optional but useful) ----------
    @app.exception_handler(mongo_errors.ConnectionFailure)
    async def mongo_connection_failure_handler(request: Request, exc: mongo_errors.ConnectionFailure):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"error": {"type": "ConnectionFailure", "detail": "Failed to connect to database."}},
        )

    # ---------- Last-resort fallback ----------
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": {"type": "ServerError", "detail": "Internal server error"}},
        )
