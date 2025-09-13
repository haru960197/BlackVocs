from fastapi import APIRouter, Depends, Response, Request
from pymongo.database import Database
from repositories.session import get_db

import schemas.auth_schemas as auth_schemas
import schemas.common_schemas as common_schemas

from services.auth_service import AuthService
from utils.auth_utils import create_access_token, get_user_id_from_cookie

router = APIRouter(prefix="/user", tags=["auth"], responses=common_schemas.COMMON_ERROR_RESPONSES)

@router.post(
    "/sign_in",
    operation_id="signin",
    response_model=auth_schemas.SignInResponse,
)
async def sign_in(
    payload: auth_schemas.SignInRequest,
    response: Response,
    db: Database = Depends(get_db),
):
    """
    Sign in and set JWT cookie.
    """
    svc = AuthService(db)
    user = svc.sign_in(payload.username_or_email, payload.password)
    token = create_access_token(str(user["_id"]))

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
    operation_id="signup",
    response_description="sign up new user",
    response_model=auth_schemas.SignUpResponse,
)
async def signup(
    payload: auth_schemas.SignUpRequest, 
    db: Database = Depends(get_db)
):
    """
    Create a new user.
    """

    svc = AuthService(db)
    inserted_id = svc.signup(payload.username, payload.email, payload.password)
    return auth_schemas.SignUpResponse(id=inserted_id)


@router.post(
    "/sign_out",
    operation_id="signout", 
    response_description="sign out of the user account",
)
async def signout(response: Response):
    """
    Delete JWT cookie and redirect.
    """

    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="none",
        secure=True,
    )
    return { "message": "Successfully signed out" }

@router.get(
    "/signed_in_check", 
    operation_id="signed_in_check", 
    response_model=auth_schemas.SignedInCheckResponse,
) 
async def signed_in_check(request: Request): 
    user_id = await get_user_id_from_cookie(request)
    return auth_schemas.SignedInCheckResponse(signed_in=True, user_id=user_id)
