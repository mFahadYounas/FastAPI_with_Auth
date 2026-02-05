from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer


load_dotenv()

ACCESS_TOKEN_EXPIRES_MINS = 15
ALGORITHM = "HS256"
jwt_secret_key = os.environ.get("JWT_SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expiry = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINS)
    )
    to_encode.update({"exp": expiry})

    if not jwt_secret_key:
        raise ValueError("Could not encode JWT: JWT Secret Key not available!")

    encoded_jwt = jwt.encode(to_encode, jwt_secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict | None:
    if not jwt_secret_key:
        raise ValueError("Could not decode JWT: JWT Secret Key not available!")
    try:
        payload = jwt.decode(token, jwt_secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError as error:
        print(f"JWT Error: {error}")
        return None
