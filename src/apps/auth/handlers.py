import bcrypt
from settings.setting import settings
from itsdangerous import URLSafeTimedSerializer, BadSignature
from src.apps.auth.schemas import TokenData
from src.schemas import EmailField
from fastapi import HTTPException
import jwt
from typing import Any




class Handlers:
    def __init__(self):
        self.serializer: URLSafeTimedSerializer = URLSafeTimedSerializer(secret_key=settings.secret_key.get_secret_value())

    async def get_hashed_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        bytes_password = password.encode("utf-8")
        hashed_password = bcrypt.hashpw(password=bytes_password, salt=salt)
        return hashed_password.decode("utf-8")

    async def compare_passwords(self, raw_password: str, hash_password: str) -> bool:
        return bcrypt.checkpw(password=raw_password.encode('utf-8'), hashed_password=hash_password.encode('utf-8'))

        
    
    async def create_verify_token(self, email: EmailField) -> str: 
        return self.serializer.dumps(email)
    
    async def load_verify_token(self, token: str) -> EmailField:
        try:
            email = self.serializer.loads(token)
            return email
        except BadSignature:
            raise HTTPException(400, detail="Cant falid token.")
        
    async def create_token(self, token_data: TokenData) -> str:
        payload = {"sub": token_data.ID, "type": token_data.token_type.value, "exp": token_data.expire}
        return jwt.encode(algorithm="HS256", payload=payload, key=settings.secret_key.get_secret_value())
    
    async def decode_token(self, token: str) -> dict[str, Any]: 
        try:
            return jwt.decode(jwt=token, key=settings.secret_key.get_secret_value(), algorithms=["HS256"])
        except jwt.exceptions.InvalidSignatureError:
            raise HTTPException(401, "Token not invalid.")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(401, "Token expired.")

    