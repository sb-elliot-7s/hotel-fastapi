from fastapi import Depends

from account.token_service import TokenService
from database import hotel_database
from permissions import AccountPermission
from token_service_data import token_service_data
from .hotel_repositories import HotelRepositories

hotel_collection = hotel_database.hotel


async def get_hotel_collection(): yield hotel_collection


async def get_account(
        account=Depends(
            AccountPermission(
                token_service=TokenService(**token_service_data)
            ).get_owner_user
        )
):
    yield account


async def get_service_data(_hotel_collection=Depends(get_hotel_collection)):
    yield {
        'repository': HotelRepositories(hotel_collection=_hotel_collection)
    }
