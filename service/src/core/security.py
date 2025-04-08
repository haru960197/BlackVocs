def create_access_token(
    payload: schemas.TokenPayload,
    expires_delta: timedelta | None = None,
):
    if expires_delta:
        exp = datetime.now(UTC) + expires_delta
    else:
        exp = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {key: value for key, value in payload}
    to_encode.update({"exp": exp})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_password_hash(password: str) -> str:
    pass

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pass