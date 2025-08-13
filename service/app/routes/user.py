from fastapi import Response, HTTPException, status, Depends, APIRouter, Request
from fastapi.responses import RedirectResponse
import core.config as config
import utils.user as auth_utils
from jwt_auth import AuthJwtCsrt
import schemas.common_schemas as common_schemas
from repositories.session import get_db
import schemas.auth as user_schemas
import models.user as user_model
from pymongo.database import Database

router = APIRouter()
auth = AuthJwtCsrt()
JWT_KEY = config.JWT_KEY

@router.post(
    "/user/signin", 
    operation_id="signin_user",
    response_description="sign in user",
    response_model=user_schemas.SigninResponse, 
    status_code=status.HTTP_201_CREATED,
    responses=common_schemas.COMMON_ERROR_RESPONSES
)
async def signin(
    signin_data: user_schemas.SigninRequest,
    response: Response,
    db: Database = Depends(get_db),
):
    """
    sign in user
    temporal token is created, and set on cookie
    """

    users_collection = db[config.USER_COLLECTION_NAME]

    user = users_collection.find_one({"username": signin_data.username})
    if not user or not auth.verify_pw(signin_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = auth_utils.create_access_token(str(user["_id"]))

    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        samesite="none",
        secure=True
    )

    return user_schemas.SigninResponse(access_token=token, token_type="bearer")

# signup
@router.post(
    "/user/signup",
    operation_id="signup_user",
    response_description="add new user", 
    response_model=user_schemas.SignupResponse, 
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False, 
    responses=common_schemas.COMMON_ERROR_RESPONSES
)
async def signup(user_data: user_schemas.SignupRequest, db: Database = Depends(get_db)):
    """
    insert a new user record
    """
    users_collection = db[config.USER_COLLECTION_NAME]

    if users_collection.find_one({"username": user_data.username}):
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_pw = auth.generate_hashed_pw(user_data.password)

    user_in_db = user_model.UserInDB(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.username,
        hashed_password=hashed_pw,
        disabled=False
    )

    result = users_collection.insert_one(user_in_db.dict())

    return user_schemas.SignupResponse (
        _id=str(result.inserted_id),
        username=user_in_db.username,
        email=user_in_db.email,
        full_name=user_in_db.full_name,
        disabled=user_in_db.disabled
    )

@router.get(
    "/user/signout",
    operation_id="signout_user",
    response_description="sign out of the user account", 
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,  
    responses=common_schemas.COMMON_ERROR_RESPONSES
)
async def signout():
    response = RedirectResponse(url="/")  
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="none",
        secure=True
    )
    return response

