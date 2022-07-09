from datetime import datetime, timedelta
from .interfaces.token_interface import TokenServiceInterface
from jose import jwt, JWTError
from fastapi import status
from common_exceptions import raise_exception


class TokenService(TokenServiceInterface):
    async def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token=token, key=self.secret_key, algorithms=self.algorithm)
        except JWTError:
            raise_exception(status.HTTP_401_UNAUTHORIZED,
                            'Could not validate credentials')

    async def encode_token(self, email: str) -> str:
        data = {
            'sub': email,
            'exp': datetime.utcnow() + timedelta(minutes=self.exp_time)
        }
        return jwt.encode(
            claims=data, key=self.secret_key, algorithm=self.algorithm
        )
