from .schemas import CreateBookingSchema
from .interfaces.booking_repositories_interface import \
    BookingRepositoriesInterface


class BookingService:
    def __init__(self, repository: BookingRepositoriesInterface):
        self.__repository = repository

    async def booking(self, account, apartment_id: str,
                      date_booking_data: CreateBookingSchema) -> object:
        return await self.__repository. \
            booking(account=account, apartment_id=apartment_id,
                    date_booking_data=date_booking_data)

    async def cancel_booking(self, account, booking_id: str):
        return await self.__repository \
            .cancel_booking(account=account, booking_id=booking_id)

    async def get_info_booking(self, booking_id: str, account):
        return await self.__repository \
            .get_info_booking(booking_id=booking_id, account=account)
