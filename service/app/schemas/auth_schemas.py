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
class SignupRequest(User):
    password: str

class SignupResponse(User):
    id: str = Field(..., alias="_id")
    class Config:
        allow_population_by_field_name = True
