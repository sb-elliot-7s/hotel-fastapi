from fastapi import APIRouter, Depends, status
from permissions import AccountPermission
from account.token_service import TokenService
from token_service_data import token_service_data
from .deps import get_booking_collection
from .services import BookingService
from .repositories import BookingRepositories
from hotel_service.apartment.deps import get_apartment_collection
from .calculate_days import CalculateDays
from .schemas import CreateBookingSchema, BookingSchema

booking_router = APIRouter(prefix='/booking', tags=['booking'])


async def get_account(
        account=Depends(AccountPermission(
            token_service=TokenService(**token_service_data)
        ).get_current_user)
):
    yield account


async def get_repository_service(
        booking_collection=Depends(get_booking_collection),
        apartment_collection=Depends(get_apartment_collection)
):
    yield {
        'repository': BookingRepositories(
            booking_collection=booking_collection,
            apartment_collection=apartment_collection,
            calculating_days_service=CalculateDays(),
        )
    }


@booking_router.post('/{apartment_id}', status_code=status.HTTP_201_CREATED,
                     response_model=BookingSchema, response_model_by_alias=False)
async def booking(apartment_id: str, date_booking_data: CreateBookingSchema,
                  account=Depends(get_account),
                  repository_service=Depends(get_repository_service)):
    return await BookingService(**repository_service) \
        .booking(apartment_id=apartment_id, account=account, date_booking_data=date_booking_data)


@booking_router.patch('/{booking_id}', status_code=status.HTTP_200_OK,
                      response_model=BookingSchema, response_model_by_alias=False)
async def cancel_booking(booking_id: str, account=Depends(get_account),
                         repository_service=Depends(get_repository_service)):
    return await BookingService(**repository_service) \
        .cancel_booking(account=account, booking_id=booking_id)


@booking_router.get('/{booking_id}', status_code=status.HTTP_200_OK, response_model=BookingSchema,
                    response_model_by_alias=False)
async def get_info_booking(
        booking_id: str, account=Depends(get_account),
        repository_service=Depends(get_repository_service)):
    return await BookingService(**repository_service) \
        .get_info_booking(booking_id=booking_id, account=account)
