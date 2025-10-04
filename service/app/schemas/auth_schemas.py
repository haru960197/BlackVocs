import re
from typing import Annotated
from pydantic import BaseModel, SecretStr, StringConstraints, Field, ConfigDict, field_validator

Username = Annotated[str, StringConstraints(min_length=3, max_length=25, strip_whitespace=True)]
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$#!%*?&]{8,25}$")

# --- sign in ---
class SignInRequest(BaseModel):
    username: str = Field(validation_alias="userName", serialization_alias="userName")
    password: SecretStr 
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("password")
    @classmethod
    def validate_password_for_signin(cls, v: SecretStr) -> SecretStr:
        raw = v.get_secret_value()
        if len(raw) < 8:
            raise ValueError("パスワードは8文字以上で入力してください")
        if len(raw) > 25:
            raise ValueError("パスワードは25文字以下で入力してください")
        if not PASSWORD_REGEX.fullmatch(raw):
            raise ValueError("パスワードは、大文字、小文字、数字をそれぞれ1つ以上含んでください。")
        return v

class SignInResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- sign up ---
class SignUpRequest(BaseModel):
    username: str = Field(validation_alias="userName", serialization_alias="userName")
    password: SecretStr 
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("password")
    @classmethod
    def validate_password_for_signin(cls, v: SecretStr) -> SecretStr:
        raw = v.get_secret_value()
        if len(raw) < 8:
            raise ValueError("パスワードは8文字以上で入力してください")
        if len(raw) > 25:
            raise ValueError("パスワードは25文字以下で入力してください")
        if not PASSWORD_REGEX.fullmatch(raw):
            raise ValueError("パスワードは、大文字、小文字、数字をそれぞれ1つ以上含んでください。")
        return v

class SignUpResponse(BaseModel):
    id: str 

# --- check if signed in ---
class SignedInCheckResponse(BaseModel):
    user_id: str 
