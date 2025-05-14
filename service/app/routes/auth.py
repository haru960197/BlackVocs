from datetime import timedelta 
from fastapi import Request, Response, HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import config
from db.session import get_db
from schemas.user_schemas import  (
    User,
    UserInDB,
    Token,
    TokenData,
) 
from utils.auth_utils import AuthJwtCsrt

router = APIRouter()
auth = AuthJwtCsrt()

JWT_KEY = config.JWT_KEY
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# test用データベース、後で消す
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}
    
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB.model_validate(user_dict)

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

async def get_current_user(token: str = Depends(get_token_from_cookie_or_header)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = auth.decode_jwt(token)
        print(username)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except HTTPException:
        raise credentials_exception
    
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/token", response_model = Token)
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.encode_jwt(user.username, expires_delta=access_token_expires)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        samesite="none",  
        secure=True        
    )

    return Token(access_token=access_token, token_type="bearer")

# get user from cookie
@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# DB test
@router.post("/DBtest", status_code=200)
def post_item_in_box(item: str):
    # dbというデータベースを取得
    db = get_db()
    # データベースにデータを追加
    result = db["box"].insert_one({"item": item})
    return {"id": str(result.inserted_id)}