from fastapi import Depends

from account.token_service import TokenService
from database import hotel_database
from permissions import AccountPermission
from token_service_data import token_service_data
from hotel_service.apartment.deps import get_apartment_collection
from .repositories import RatingRepositories

rating_collection = hotel_database.rating


async def get_rating_collection(): yield rating_collection


async def get_customer_account(
        account=Depends(
            AccountPermission(
                token_service=TokenService(**token_service_data)
            ).get_current_user)
):
    yield account


async def get_service_data(
        _rating_collection=Depends(get_rating_collection),
        _apartment_collection=Depends(get_apartment_collection)
):
    yield {
        'repository': RatingRepositories(
            rating_collection=_rating_collection,
            apartment_collection=_apartment_collection
        )
    }
