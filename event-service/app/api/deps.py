from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.infrastructure.db.session import get_session
from app.infrastructure.security.jwt_validator import JWTValidator

oauth2 = OAuth2PasswordBearer(tokenUrl="none")


async def get_current_user(token: str = Depends(oauth2)):
    validator = JWTValidator()

    payload = validator.validate_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


async def get_db_session():
    async for session in get_session():
        yield session
