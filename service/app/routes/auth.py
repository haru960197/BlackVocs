from fastapi import APIRouter, Depends, Response, status
from pymongo.database import Database
from core.oid import PyObjectId
from repositories.session import get_db
from services.auth_service import AuthService
import schemas.auth_schemas as auth_schemas
import schemas.common_schemas as common_schemas

router = APIRouter(prefix="/user", tags=["auth"], responses=common_schemas.COMMON_ERROR_RESPONSES)

@router.post(
    "/sign_in",
    operation_id="sign_in",
    status_code=status.HTTP_200_OK
)
async def sign_in(
    payload: auth_schemas.SignInRequest,
    response: Response,
    db: Database = Depends(get_db),
):
    svc = AuthService(db)

    access_token = svc.create_access_token(payload)

    response.set_cookie(
        key="access_token",
        value=access_token,  
        httponly=True,
        samesite="none",
        secure=True,
    )
    
    return

@router.post(
    "/sign_up",
    operation_id="sign_up",
    status_code=status.HTTP_200_OK
)
async def sign_up(
    payload: auth_schemas.SignUpRequest, 
    db: Database = Depends(get_db)
):
    svc = AuthService(db)
    svc.sign_up(payload)
    return

@router.post(
    "/sign_out",
    operation_id="sign_out", 
    status_code=status.HTTP_204_NO_CONTENT
)
async def sign_out(response: Response):
    """
    Delete JWT cookie and redirect.
    """
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="none",
        secure=True,
    )
    return

@router.get(
    "/signed_in_check", 
    operation_id="signed_in_check", 
    response_model=auth_schemas.SignedInCheckResponse,
) 
async def signed_in_check(user_id: PyObjectId = Depends(AuthService.get_user_id_from_cookie)): 
    """
    return user_id if signed in, else raise TokenInvalidError or TokenInvalidError
    """
    return auth_schemas.SignedInCheckResponse(user_id=str(user_id))
