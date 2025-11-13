from pydantic import BaseModel

# --- sign in ---
class SignInRequest(BaseModel):
    username: str
    password: str

class SignInResponse(BaseModel):
    access_token: str

# --- sign up ---
class SignUpRequest(BaseModel):
    username: str
    password: str

# --- check if signed in ---
class SignedInCheckResponse(BaseModel):
    user_id: str 
