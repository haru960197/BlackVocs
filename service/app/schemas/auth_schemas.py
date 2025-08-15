from pydantic import BaseModel, EmailStr, Field

# user --------------------------------------
class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    disabled: bool = False

# sign in -------------------------------------
class SigninRequest(BaseModel):
    username_or_email: str
    password: str

class SigninResponse(BaseModel):
    access_token: str
    token_type: str

# sign up -------------------------------------
class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class SignupResponse(BaseModel):
    id: str

class SignedInCheckResponse(BaseModel):
    signed_in: bool
    user_id: str | None = None
