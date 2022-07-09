from fastapi import Depends

from account.token_service import TokenService
from database import hotel_database
from permissions import AccountPermission
from token_service_data import token_service_data
from hotel_service.apartment.deps import get_apartment_collection
from .calculate_days import CalculateDays
from .repositories import BookingRepositories

booking_collection = hotel_database.booking


async def get_booking_collection(): yield booking_collection


async def get_account(
        account=Depends(AccountPermission(
            token_service=TokenService(**token_service_data)
        ).get_current_user)
):
    yield account


async def get_repository_service(
        _booking_collection=Depends(get_booking_collection),
        _apartment_collection=Depends(get_apartment_collection)
):
    yield {
        'repository': BookingRepositories(
            booking_collection=_booking_collection,
            apartment_collection=_apartment_collection,
            calculating_days_service=CalculateDays(),
        )
    }
