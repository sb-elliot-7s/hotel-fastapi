from datetime import datetime
from .interfaces.repositories_interface import AccountRepositoryInterface
from .schemas import CreateAccountSchema
from common_exceptions import raise_exception
from fastapi import status


class AccountRepository(AccountRepositoryInterface):
    def __init__(self, account_collection):
        self._account_collection = account_collection

    async def __get_account(self, _filter: dict):
        if (account := await self._account_collection.find_one(filter=_filter)) is None:
            return False
        return account

    async def __create_account_and_return(self, document: dict):
        result = await self._account_collection.insert_one(document=document)
        return await self.__get_account({'_id': result.inserted_id})

    async def create_account(self, password: str, account_data: CreateAccountSchema):
        document = {
            'password': password,
            'created': datetime.utcnow(),
            'updated': None,
            'is_active': True,
            **account_data.transform_dict
        }
        return await self.__create_account_and_return(document=document)

    async def get_account_by_email(self, email: str):
        if (account := await self.__get_account({'email': email})) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Account not found')
        return account
