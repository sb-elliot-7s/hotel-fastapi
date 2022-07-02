from abc import ABC, abstractmethod

from booking.schemas import CreateBookingSchema


class BookingRepositoriesInterface(ABC):

    @abstractmethod
    async def booking(self, account, apartment_id: str,
                      date_booking_data: CreateBookingSchema):
        pass

    @abstractmethod
    async def cancel_booking(self, account, booking_id: str): pass

    @abstractmethod
    async def get_info_booking(self, booking_id: str, account): pass
