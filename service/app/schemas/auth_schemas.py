from pydantic import BaseModel, EmailStr, Field

# user --------------------------------------
class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    disabled: bool = False

# sign in -------------------------------------
class SignInRequest(BaseModel):
    username_or_email: str
    password: str

class SignInResponse(BaseModel):
    access_token: str
    token_type: str

# sign up -------------------------------------
class SignUpRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class SignUpResponse(BaseModel):
    id: str

class SignedInCheckResponse(BaseModel):
    signed_in: bool
    user_id: str | None = None
