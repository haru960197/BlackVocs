from fastapi import Response, HTTPException, status, Depends, APIRouter, Request
from fastapi.responses import RedirectResponse
import core.config as config
import utils.user as auth_utils
from jwt_auth import AuthJwtCsrt
from db.session import get_db
from schemas.user import  (
    User,
    UserCreate,
    Token,
    SigninRequest,
) 
import models.user as user_model
from pymongo.database import Database

router = APIRouter()
auth = AuthJwtCsrt()
JWT_KEY = config.JWT_KEY

@router.post("/user/signin", response_model=Token)
async def signin(
    signin_data: SigninRequest,
    response: Response,
    db: Database = Depends(get_db),
):
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

    return Token(access_token=token, token_type="bearer")


# signup
@router.post("/user/signup", response_model=User, status_code=201)
async def signup(user_data: UserCreate, db: Database = Depends(get_db)):
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

    return User(
        id=str(result.inserted_id),
        username=user_in_db.username,
        email=user_in_db.email,
        full_name=user_in_db.full_name,
        disabled=user_in_db.disabled
    )

@router.get("/user/signout")
async def signout():
    response = RedirectResponse(url="/")  
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="none",
        secure=True
    )
    return response

# get current user id from cookie
@router.get("/user/me")
async def get_me(current_user_id: str = Depends(auth_utils.get_user_id_from_cookie)):
    return current_user_id
