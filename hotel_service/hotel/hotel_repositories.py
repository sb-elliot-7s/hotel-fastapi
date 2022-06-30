from bson import ObjectId
from .interfaces.hotel_repositories_interface import HotelRepositoriesInterface
from .hotel_schemas import CreateHotelSchema, HotelSchema, QueryHotelSchema, UpdateHotelSchema
from common_exceptions import raise_exception
from fastapi import status

from .query_service import QueryService


class HotelRepositories(HotelRepositoriesInterface):
    def __init__(self, hotel_collection):
        self._hotel_collection = hotel_collection

    async def __get_hotel(self, hotel_id: str) -> HotelSchema:
        if (hotel := await self._hotel_collection.find_one({'_id': ObjectId(hotel_id)})) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Hotel not found')
        return hotel

    async def create_hotel(self, hotel: CreateHotelSchema, account) -> HotelSchema:
        document = {
            'account_id': account.id,
            'apartments': [],
            'available_count_of_apartments': 0,
            **hotel.transformed_dict
        }
        result = await self._hotel_collection.insert_one(document=document)
        return await self.__get_hotel(hotel_id=result.inserted_id)

    async def remove_hotel(self, hotel_id: str, account):
        hotel_filter = {'_id': ObjectId(hotel_id), 'account_id': account.id}
        if (hotel := await self._hotel_collection.find_one_and_delete(filter=hotel_filter)) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Hotel not found')
        return hotel

    async def update_hotel(self, hotel_id: str, account, hotel: UpdateHotelSchema) -> HotelSchema:
        hotel_update = hotel.transformed_dict
        if 'address' in hotel.transformed_dict and (address := hotel_update.pop('address')):
            hotel_update.update({f'address.{k}': v for k, v in address.items()})
        hotel_update = {'$set': hotel_update}
        hotel_filter = {'_id': ObjectId(hotel_id), 'account_id': account.id}
        if (hotel := await self._hotel_collection
                .find_one_and_update(filter=hotel_filter, update=hotel_update, return_document=True)) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Hotel not found')
        return hotel

    async def show_detail_hotel(self, hotel_id: str) -> HotelSchema:
        return await self.__get_hotel(hotel_id=hotel_id)

    async def show_hotels(self, query_data: QueryHotelSchema,
                          limit: int = 20, skip: int = 0) -> list[HotelSchema]:
        query = QueryService().prepare_query_data(query_data=query_data)
        cursor = self._hotel_collection \
            .find(query) \
            .sort('avg_rating', -1) \
            .skip(skip) \
            .limit(limit)
        return [hotel async for hotel in cursor]
