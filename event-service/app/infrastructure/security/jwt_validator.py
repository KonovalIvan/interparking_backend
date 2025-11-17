from jose import jwt

SECRET = "DEV_SECRET"


class JWTValidator:
    def validate_access_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET, algorithms=["HS256"])
            return payload
        except Exception:
            return None
