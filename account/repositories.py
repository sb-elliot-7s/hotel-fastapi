import uuid
from datetime import datetime
from .interfaces.repositories_interface import AccountRepositoryInterface
from .schemas import CreateAccountSchema
from common_exceptions import raise_exception
from fastapi import status

from stripe import Customer
from configs import get_configs
from payment.decorators import stripe_decorator_error


class AccountRepository(AccountRepositoryInterface):
    def __init__(self, account_collection):
        self._account_collection = account_collection

    async def __get_account(self, _filter: dict):
        if (account := await self._account_collection.find_one(filter=_filter)) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Account not found')
        return account

    @staticmethod
    @stripe_decorator_error
    async def __create_stripe_account(account_data: CreateAccountSchema):
        return Customer.create(
            api_key=get_configs().stripe_api_key,
            idempotency_key=str(uuid.uuid4()),
            email=account_data.email,
            phone=account_data.phone
        )

    async def __create_account_and_return(self, document: dict):
        result = await self._account_collection.insert_one(document=document)
        return await self.__get_account({'_id': result.inserted_id})

    async def create_account(self, password: str, account_data: CreateAccountSchema):
        stripe_account = await self.__create_stripe_account(account_data=account_data)
        document = {
            'password': password,
            'created': datetime.utcnow(),
            'updated': None,
            'is_active': True,
            'stripe_account_id': stripe_account['id'],
            **account_data.transform_dict
        }
        return await self.__create_account_and_return(document=document)

    async def get_account_by_email(self, email: str):
        return await self._account_collection.find_one(filter={'email': email})
