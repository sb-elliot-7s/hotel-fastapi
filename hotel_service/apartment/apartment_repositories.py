from datetime import datetime
from bson import ObjectId
from .apartment_schemas import CreateApartmentSchema, ApartmentSchema, ApartmentQuerySchema, \
    UpdateApartmentSchema
from .interfaces.apartment_repositories_interface import ApartmentRepositoriesInterface
from common_exceptions import raise_exception
from fastapi import status
from .apt_query_service import ApartmentQueryService


class ApartmentRepositories(ApartmentRepositoriesInterface):
    def __init__(self, apartment_collection):
        self._apartment_collection = apartment_collection

    async def __get_apartment(self, apartment_id: str):
        if (apartment := await self._apartment_collection.find_one({'_id': ObjectId(apartment_id)})) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Apartment not found')
        return apartment

    async def create_apartment(self, account, hotel_station,
                               apartment: CreateApartmentSchema):
        document = {
            'account_id': account.id, 'created': datetime.utcnow(),
            'updated': None, **apartment.dict(exclude_none=True)
        }
        result = await self._apartment_collection.insert_one(document=document)
        new_apartment = await self.__get_apartment(apartment_id=result.inserted_id)
        if (_ := await hotel_station.find_one_and_update(
                filter={
                    '_id': ObjectId(apartment.hotel_id),
                    'account_id': account.id,
                    '$expr': {'$lt': [{'$size': '$apartments'}, '$count_of_apartments']}
                },
                update={'$inc': {'available_count_of_apartments': 1}, '$push': {'apartments': new_apartment}},
                return_document=True
        )) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Hotel not found or unable to add apartment to hotel')
        return new_apartment

    async def remove_apartment(self, account, apartment_id: str):
        if (apt := await self._apartment_collection.find_one_and_delete(
                {'_id': ObjectId(apartment_id), 'account_id': account.id})) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Apartment not found')
        return apt

    async def update_apartment(self, account, apartment_id: str,
                               apartment: UpdateApartmentSchema):
        apartment_filter = {'_id': ObjectId(apartment_id), 'account_id': account.id}
        apartment_update = {'$set': apartment.transformed_dict}
        if (apartment := await self._apartment_collection.find_one_and_update(
                filter=apartment_filter, update=apartment_update, return_document=True)) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Apartment not found')
        return ApartmentSchema(**apartment)

    async def detail_apartment(self, apartment_id: str):
        return ApartmentSchema(**await self.__get_apartment(apartment_id=apartment_id))

    async def all_available_apartments(self, hotel_id: str, query_data: ApartmentQuerySchema,
                                       skip: int = 0, limit: int = 20):
        query = ApartmentQueryService().prepare_query_data(data=query_data)
        cursor = self._apartment_collection \
            .find(query) \
            .sort('created', -1) \
            .skip(skip) \
            .limit(limit)
        return [apt async for apt in cursor]
