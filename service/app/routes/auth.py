from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.responses import RedirectResponse
from pymongo.database import Database
from repositories.session import get_db
import schemas.auth_schemas as auth_schemas
from services.auth_service import AuthService
from utils.auth_utils import create_access_token, get_user_id_from_cookie
router = APIRouter(prefix="/user", tags=["auth"])

@router.post(
    "/signin",
    operation_id="signin",
    response_description="sign in user",
    response_model=auth_schemas.SigninResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signin(
    payload: auth_schemas.SigninRequest,
    response: Response,
    db: Database = Depends(get_db),
):
    """
    Sign in and set JWT cookie.
    """
    svc = AuthService(db)
    try:
        user = svc.signin(payload.username_or_email, payload.password)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = create_access_token(str(user["_id"]))

    response.set_cookie(
        key="access_token",
        value=token,  
        httponly=True,
        samesite="none",
        secure=True,
    )
    return auth_schemas.SigninResponse(access_token=token, token_type="bearer")


@router.post(
    "/signup",
    operation_id="signup",
    response_description="add new user",
    response_model=auth_schemas.SignupResponse,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def signup(payload: auth_schemas.SignupRequest, db: Database = Depends(get_db)):
    """
    Create a new user.
    """
    svc = AuthService(db)
    try:
        inserted_id, _ = svc.signup(payload.username, payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return auth_schemas.SignupResponse(
        id=str(inserted_id)
    )


@router.get(
    "/signout",
    operation_id="signout", 
    response_description="sign out of the user account",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
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
    status_code=status.HTTP_200_OK,
    response_model=auth_schemas.SignedInCheckResponse,
) 
async def signed_in_check(request: Request): 
    try: 
        user_id = await get_user_id_from_cookie(request)
        return auth_schemas.SignedInCheckResponse(signed_in=True, user_id=user_id)
    except Exception:
        return auth_schemas.SignedInCheckResponse(signed_in=False, user_id=None)
