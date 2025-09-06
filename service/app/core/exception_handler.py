from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from core.errors import UnauthorizedError

def register_exception_handlers(app):
    @app.exception_handler(UnauthorizedError)
    async def _unauth_handler(request: Request, exc: UnauthorizedError): 
        return JSONResponse(
            status_code=401,
            content={"error": {"type": exc.__class__.__name__, "detail": str(exc) or "Unauthorized"}},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "type": "HTTPException",
                    "detail": exc.detail,
                }
            },
        )

