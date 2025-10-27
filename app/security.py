from datetime import timedelta, datetime, timezone
from jose import jwt
from os import environ

ACCESS_TOKEN_EXPIRES_MINS = 15
ALGORITHM = "HS256"
jwt_secret_key = environ.get("JWT_SECRET_KEY")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expiry = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINS)
    )
    to_encode.update({"exp": expiry})

    if not jwt_secret_key:
        raise ValueError("Could not encode JWT: JWT Secret Key not available")

    encoded_jwt = jwt.encode(to_encode, jwt_secret_key, algorithm=ALGORITHM)
    return encoded_jwt
