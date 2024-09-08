from datetime import datetime, timedelta
from jose import JWTError, jwt
from app import models, schemas

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1000


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception, db):
    try:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            print(username)
            token_user = db.query(models.User).filter(models.User.username == username, models.User.is_active == True).first()
            print("user:", token)
            if username is None:
                print("apikey:", token)
                raise credentials_exception
            token_data = token_user
            return token_data
        except JWTError:
            # If the token is not a JWT, check if it is an API key
            print("JWTError: ", token)
            api_key_user = db.query(models.APIKey).filter(models.APIKey.key == token, models.APIKey.status == 1).first()
            if api_key_user:
                return api_key_user
            raise credentials_exception
    except JWTError:
        raise credentials_exception
