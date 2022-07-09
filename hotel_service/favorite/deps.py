from fastapi import Depends

from account.token_service import TokenService
from database import hotel_database
from .favorite_repositories import FavoriteRepositories
from permissions import AccountPermission
from token_service_data import token_service_data

favorite_collection = hotel_database.favorite


async def get_favorite_collection(): yield favorite_collection


async def get_account(account=Depends(
    AccountPermission(token_service=TokenService(
        **token_service_data)
    ).get_current_user
)):
    yield account


async def get_service_data(
        _favorite_collection=Depends(get_favorite_collection)
):
    yield {
        'repository': FavoriteRepositories(
            favorite_collection=_favorite_collection)
    }
