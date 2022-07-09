from fastapi import Depends
from passlib.context import CryptContext
from account.password_service import PasswordService
from account.repositories import AccountRepository
from account.token_service import TokenService
from configs import get_configs
from database import hotel_database

account_collection = hotel_database.account


async def get_account_collection(): yield account_collection


async def get_account_service(
        _account_collection=Depends(get_account_collection)):
    yield {
        'token_service': TokenService(
            secret_key=get_configs().secret_key,
            algorithm=get_configs().algorithm,
            exp_time=get_configs().exp_time
        ),
        'password_service': PasswordService(
            context=CryptContext(schemes=['bcrypt'], deprecated='auto')
        ),
        'repository': AccountRepository(account_collection=_account_collection)
    }
