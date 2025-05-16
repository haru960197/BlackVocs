from datetime import timedelta 
from fastapi import Request, Response, HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import config
from db.session import get_db
from schemas.user_schemas import  (
    User,
    UserInDB,
    UserCreate,
    Token,
    TokenData,
    LoginRequest,
) 
from jwt_auth import AuthJwtCsrt
from pymongo.database import Database

router = APIRouter()
auth = AuthJwtCsrt()

JWT_KEY = config.JWT_KEY
USER_COLLECTION_NAME = config.USER_COLLECTION_NAME
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_user(db: Database, username: str) -> UserInDB | None:
    user_data = db[USER_COLLECTION_NAME].find_one({"username": username})
    if user_data:
        return UserInDB.model_validate(user_data)
    return None

# using verify_pw function defined in auth jwt class
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not auth.verify_pw(password, user.hashed_password):
        return False
    return user

async def get_token_from_cookie_or_header(
    request: Request,
    header_token: str = Depends(oauth2_scheme),
):
    token = request.cookies.get("access_token")
    if token:
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]
        return token
    return header_token

async def get_current_user(
    token: str = Depends(get_token_from_cookie_or_header),
    db: Database = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = auth.decode_jwt(token)
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except HTTPException:
        raise credentials_exception

    user = get_user(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def create_access_token(username: str) -> str:
    expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = auth.encode_jwt(username, expires_delta=expire)
    return token

@router.post("/user/signin", response_model=Token)
async def login(
    login_data: LoginRequest,
    response: Response,
    db: Database = Depends(get_db),
):
    users_collection = db[USER_COLLECTION_NAME]

    user = users_collection.find_one({"username": login_data.username})
    if not user or not auth.verify_pw(login_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token(user["username"])

    # needed?
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
    users_collection = db[USER_COLLECTION_NAME]

    existing_user = users_collection.find_one({"username": user_data.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_pw = auth.generate_hashed_pw(user_data.password)

    user_dict = {
        "username": user_data.username,
        "email": user_data.email,
        "full_name": user_data.username,  
        "hashed_password": hashed_pw,
        "disabled": False,
    }

    result = users_collection.insert_one(user_dict)

    user_dict.pop("hashed_password")  
    user_dict["id"] = str(result.inserted_id)

    return User(**user_dict)

# get user from cookie
@router.get("/user/get_user", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# Token
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Database = Depends(get_db),
):
    users_collection = db[USER_COLLECTION_NAME]

    # ユーザー検索
    user_data = users_collection.find_one({"username": form_data.username})
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not auth.verify_pw(form_data.password, user_data["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user_data["username"])
    return Token(access_token=access_token, token_type="bearer")