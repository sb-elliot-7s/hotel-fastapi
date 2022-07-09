import json
from datetime import datetime

from bson import ObjectId
from common_exceptions import raise_exception
from fastapi import status
from database import client
from common_aggregation_mixin import AggregationMixin
from .interfaces.booking_repositories_interface import \
    BookingRepositoriesInterface
from .calculate_days import CalculateDays
import calendar
from producer import producer

from .schemas import CreateBookingSchema, PaymentStatus


class BookingRepositories(AggregationMixin, BookingRepositoriesInterface):
    def __init__(self, booking_collection, apartment_collection,
                 calculating_days_service: CalculateDays):
        self.__calculating_days_service = calculating_days_service
        self.__apartment_collection = apartment_collection
        self.__booking_collection = booking_collection

    async def __get_booking(self, booking_id: str, account_id: str):
        if not (booking := await self.__booking_collection.find_one(
                {'_id': ObjectId(booking_id), 'account_id': account_id})):
            raise_exception(status.HTTP_404_NOT_FOUND,
                            f'Booking {booking_id} not found')
        return booking

    async def __update_apartment(self, apartment_id: str, is_booked: bool):
        _filter = self.filter_objects(_id=ObjectId(apartment_id),
                                      is_booked=not is_booked)
        _update = self.set_document(document={'is_booked': is_booked})
        if not (apartment := await self.__apartment_collection
                .find_one_and_update(filter=_filter,
                                     update=_update,
                                     return_document=True)):
            raise_exception(
                status.HTTP_404_NOT_FOUND,
                f'Apartment {apartment_id} not found'
            )
        return apartment

    @staticmethod
    async def __produce_value(value: int, hotel_id: str):
        await producer.send(
            'hotel-apt-count',
            value=json.dumps(
                {
                    'available_count_of_apartments': value,
                    'hotel_id': hotel_id
                }
            ).encode('utf-8')
        )

    async def booking(self, account, apartment_id: str,
                      date_booking_data: CreateBookingSchema):
        # need replicas and add session to update, insert method
        async with await client.start_session() as session:
            async with session.start_transaction():
                apartment = await self.__update_apartment(
                    apartment_id=apartment_id, is_booked=True)
                await self.__produce_value(
                    value=-1, hotel_id=apartment['hotel_id'])
                cnt_of_days_rent = await self.__calculating_days_service \
                    .calculate(check_in=date_booking_data.check_in,
                               check_out=date_booking_data.check_out)

                week_day, number_of_days_in_month = calendar \
                    .monthrange(datetime.now().year, datetime.now().month)

                total_money = cnt_of_days_rent * (
                    day_price := (month_price := apartment.get(
                        'price')) / number_of_days_in_month
                )
                document = {
                    'apartment_id': apartment_id,
                    'account_id': account.id,
                    'check_in': date_booking_data.check_in,
                    'check_out': date_booking_data.check_out,
                    'count_of_days_rent': cnt_of_days_rent,
                    'month_price': round(month_price, 2),
                    'day_price': round(day_price, 2),
                    'total_money': round(total_money, 2),
                    'payment_status': PaymentStatus.UNPAID.value,
                    'is_active': True
                }
                result = await self.__booking_collection.insert_one(
                    document=document)
                return await self.__get_booking(booking_id=result.inserted_id,
                                                account_id=account.id)

    async def cancel_booking(self, account, booking_id: str):
        # need replicas and add session to update, insert method
        async with await client.start_session() as session:
            async with session.start_transaction():
                document = {'is_active': False, 'updated': datetime.utcnow()}
                _filter = self.filter_objects(
                    _id=ObjectId(booking_id),
                    account_id=account.id,
                    is_active=True
                )
                _update = self.set_document(document=document)
                if not (booking := await self.__booking_collection
                        .find_one_and_update(filter=_filter,
                                             update=_update,
                                             return_document=True)):
                    raise_exception(status.HTTP_404_NOT_FOUND,
                                    'Booking not found')
                apt = await self.__update_apartment(
                    apartment_id=booking['apartment_id'], is_booked=False)
                await self.__produce_value(value=1, hotel_id=apt['hotel_id'])
                return booking

    async def get_info_booking(self, booking_id: str, account):
        return await self.__get_booking(booking_id=booking_id,
                                        account_id=account.id)
