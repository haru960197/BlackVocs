from pydantic import BaseModel

from models.common import PyObjectId

# --- General ---
class User(BaseModel):
    username: str
    disabled: bool = False

# --- sign in ---
class SignInRequest(User):
    password: str

class SignInResponse(BaseModel):
    access_token: str
    token_type: str

# --- sign up ---
class SignUpRequest(User):
    password: str

class SignUpResponse(BaseModel):
    id: PyObjectId

# --- sign out ---
class SignOutResponse(BaseModel): 
    msg: str

# --- check if signed in ---
class SignedInCheckResponse(BaseModel):
    user_id: PyObjectId 
