from pydantic import BaseModel

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
    id: str 

# --- sign out ---
class SignOutResponse(BaseModel): 
    msg: str

# --- check if signed in ---
class SignedInCheckResponse(BaseModel):
    user_id: str 
