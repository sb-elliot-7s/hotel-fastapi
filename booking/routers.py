from fastapi import APIRouter, Depends, status
from .services import BookingService
from .schemas import CreateBookingSchema, BookingSchema
from .deps import get_repository_service, get_account

booking_router = APIRouter(prefix='/booking', tags=['booking'])


@booking_router.post('/{apartment_id}', status_code=status.HTTP_201_CREATED,
                     response_model=BookingSchema,
                     response_model_by_alias=False)
async def booking(apartment_id: str, date_booking_data: CreateBookingSchema,
                  account=Depends(get_account),
                  repository_service=Depends(get_repository_service)):
    return await BookingService(**repository_service) \
        .booking(apartment_id=apartment_id,
                 account=account,
                 date_booking_data=date_booking_data)


@booking_router.patch('/{booking_id}', status_code=status.HTTP_200_OK,
                      response_model=BookingSchema,
                      response_model_by_alias=False)
async def cancel_booking(booking_id: str, account=Depends(get_account),
                         repository_service=Depends(get_repository_service)):
    return await BookingService(**repository_service) \
        .cancel_booking(account=account, booking_id=booking_id)


@booking_router.get('/{booking_id}', status_code=status.HTTP_200_OK,
                    response_model=BookingSchema,
                    response_model_by_alias=False)
async def get_info_booking(
        booking_id: str, account=Depends(get_account),
        repository_service=Depends(get_repository_service)):
    return await BookingService(**repository_service) \
        .get_info_booking(booking_id=booking_id, account=account)
