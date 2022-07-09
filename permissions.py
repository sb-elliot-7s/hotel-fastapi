from fastapi import Depends, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from common_exceptions import raise_exception
from account.interfaces.token_interface import TokenServiceInterface
from account.deps import get_account_collection
from account.schemas import AccountSchema
from account.account_type import AccountType


class AccountPermission:
    OAUTH_TOKEN = OAuth2PasswordBearer(tokenUrl='/account/login')

    def __init__(self, token_service: TokenServiceInterface):
        self._token_service = token_service

    async def __decode_token(self, token: str):
        payload = await self._token_service.decode_token(token=token)
        if not (email := payload.get('sub')):
            raise_exception(status.HTTP_401_UNAUTHORIZED, 'Empty sub field')
        return email

    async def __get_account(self, token, account_collection, **_filters):
        _filters.update({'email': await self.__decode_token(token=token)})
        if (account := await account_collection.find_one(
                filter=_filters)) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Account not found')
        return AccountSchema(**account)

    async def get_current_user(
            self, token: str = Depends(OAUTH_TOKEN),
            account_collection=Depends(get_account_collection)):
        return await self.__get_account(
            is_active=True, account_type=AccountType.CUSTOMER.value,
            token=token,
            account_collection=account_collection
        )

    async def get_superuser(self,
                            account_collection=Depends(get_account_collection),
                            token: str = Depends(OAUTH_TOKEN)):
        return await self.__get_account(
            is_active=True, is_superuser=True,
            account_collection=account_collection,
            account_type=AccountType.SUPERUSER.value, token=token)

    async def get_owner_user(self, token: str = Depends(OAUTH_TOKEN),
                             account_collection=Depends(
                                 get_account_collection)):
        return await self.__get_account(
            is_active=True, is_agent=True, account_type=AccountType.AGENT.value,
            token=token,
            account_collection=account_collection
        )
