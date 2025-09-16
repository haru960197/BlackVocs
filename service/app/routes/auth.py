from fastapi import APIRouter, Depends, Response
from pymongo.database import Database
from repositories.session import get_db
from services.auth_service import AuthService
import schemas.auth_schemas as auth_schemas
import schemas.common_schemas as common_schemas

router = APIRouter(prefix="/user", tags=["auth"], responses=common_schemas.COMMON_ERROR_RESPONSES)

@router.post(
    "/sign_in",
    operation_id="sign_in",
    response_model=auth_schemas.SignInResponse,
)
async def sign_in(
    payload: auth_schemas.SignInRequest,
    response: Response,
    db: Database = Depends(get_db),
):
    svc = AuthService(db)
    token = svc.sign_in(payload.username, payload.password)

    response.set_cookie(
        key="access_token",
        value=token,  
        httponly=True,
        samesite="none",
        secure=True,
    )
    return auth_schemas.SignInResponse(access_token=token, token_type="bearer")

@router.post(
    "/sign_up",
    operation_id="sign_up",
    response_description="sign up new user",
    response_model=auth_schemas.SignUpResponse,
)
async def sign_up(
    payload: auth_schemas.SignUpRequest, 
    db: Database = Depends(get_db)
):
    """
    Create a new user.
    """
    svc = AuthService(db)
    user_id = svc.sign_up(payload.username, payload.password)
    return auth_schemas.SignUpResponse(id=user_id)


@router.post(
    "/sign_out",
    operation_id="sign_out", 
    response_description="sign out of the user account",
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
    return auth_schemas.SignOutResponse(msg="Successfully signed out")

@router.get(
    "/signed_in_check", 
    operation_id="signed_in_check", 
    response_model=auth_schemas.SignedInCheckResponse,
) 
async def signed_in_check(user_id: str = Depends(AuthService.get_user_id_from_cookie)): 
    """
    return user_id if signed in, else raise TokenInvalidError or TokenInvalidError
    """
    return auth_schemas.SignedInCheckResponse(user_id=user_id)
