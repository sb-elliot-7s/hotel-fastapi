from .interfaces.repositories_interface import AccountRepositoryInterface
from .interfaces.password_interface import PasswordServiceInterface
from .interfaces.token_interface import TokenServiceInterface
from .schemas import CreateAccountSchema
from fastapi import status
from common_exceptions import raise_exception


class AuthLogic:
    def __init__(self, repository: AccountRepositoryInterface, password_service: PasswordServiceInterface,
                 token_service: TokenServiceInterface):
        self.__token_service = token_service
        self.__password_service = password_service
        self.__repository = repository

    async def save_user(self, account_data: CreateAccountSchema):
        if await self.__repository.get_account_by_email(email=account_data.email):
            raise_exception(status.HTTP_400_BAD_REQUEST, 'User with this email exists')
        hashed_password = await self.__password_service.hashed_password(plain_password=account_data.password)
        return await self.__repository \
            .create_account(password=hashed_password, account_data=account_data)

    async def _authenticate(self, email: str, password: str):
        if not (account := await self.__repository.get_account_by_email(email=email)) \
                or not await self.__password_service.verify_passwords(plain_password=password,
                                                                      hashed_password=account['password']):
            raise_exception(status.HTTP_400_BAD_REQUEST, 'Incorrect email or password')
        return account

    async def login(self, email: str, password: str):
        account = await self._authenticate(email=email, password=password)
        return {'token': await self.__token_service.encode_token(email=account['email'])}
