from abc import ABC, abstractmethod


class TokenServiceInterface(ABC):

    def __init__(self, secret_key: str, exp_time: int, algorithm: str):
        self.exp_time = exp_time
        self.algorithm = algorithm
        self.secret_key = secret_key

    @abstractmethod
    async def decode_token(self, token: str) -> dict: pass

    @abstractmethod
    async def encode_token(self, email: str) -> str: pass
