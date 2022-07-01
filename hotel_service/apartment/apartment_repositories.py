from datetime import datetime
from typing import Optional

from bson import ObjectId

from database import client
from .apartment_schemas import CreateApartmentSchema, ApartmentQuerySchema, \
    UpdateApartmentSchema, SearchApartmentSchema
from .interfaces.apartment_repositories_interface import ApartmentRepositoriesInterface
from common_exceptions import raise_exception
from fastapi import status, UploadFile
from .apt_query_service import ApartmentQueryService
from .apartment_aggregation_mixin import AggregationMixin
from image_service.image_service_interface import ImageServiceInterface


class ApartmentRepositories(AggregationMixin, ApartmentRepositoriesInterface):
    def __init__(self, apartment_collection, hotel_collection, image_service: ImageServiceInterface):
        self.__hotel_collection = hotel_collection
        self.__image_service = image_service
        self.__apartment_collection = apartment_collection

    async def __get_apartment(self, apartment_id: str):
        if (apartment := await self.__apartment_collection.find_one({'_id': ObjectId(apartment_id)})) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Apartment not found')
        return apartment

    async def __update_apartment_after_images_saved(self, apartment_id: str, images_id: list[ObjectId]):
        return await self.__apartment_collection.find_one_and_update(
            {'_id': ObjectId(apartment_id)}, {'$push': {'images': {'$each': images_id or []}}},
            return_document=True)

    async def __save_images(self, images: Optional[list[UploadFile]]):
        if images:
            return [await self.__image_service.write_image(image, image.filename) for image in images]

    async def __update_hotel(self, apartment, hotel_id: str, account_id: str):
        data = {
            'filter': {'_id': ObjectId(hotel_id), 'account_id': account_id,
                       '$expr': {'$lt': [{'$size': '$apartments'}, '$count_of_apartments']}},
            'update': {'$inc': {'available_count_of_apartments': 1}, '$push': {'apartments': apartment}},
            'return_document': True
        }
        if (_ := await self.__hotel_collection.find_one_and_update(**data)) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Hotel not found or unable to add apartment to hotel')

    async def __create_apartment(self, account, apartment: CreateApartmentSchema,
                                 images: Optional[list[UploadFile]]):
        document = {
            'account_id': account.id,
            'created': datetime.utcnow(),
            'updated': None,
            **apartment.dict(exclude_none=True)
        }
        result = await self.__apartment_collection.insert_one(document=document)
        apt = await self.__get_apartment(apartment_id=result.inserted_id)
        images_id = await self.__save_images(images=images)
        return await self.__update_apartment_after_images_saved(str(apt['_id']), images_id)

    async def create_apartment(self, account, apartment: CreateApartmentSchema,
                               images: Optional[list[UploadFile]] = None):
        apt = await self.__create_apartment(account=account, apartment=apartment, images=images)
        await self.__update_hotel(apartment=apt, hotel_id=apartment.hotel_id, account_id=account.id)
        return apt

    async def remove_apartment(self, account, apartment_id: str):
        apt_filter = {'_id': ObjectId(apartment_id), 'account_id': account.id}
        if (apt := await self.__apartment_collection.find_one_and_delete(apt_filter)) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Apartment not found')
        await self.__hotel_collection.update_one({'_id': ObjectId(apt['hotel_id'])}, {
            '$inc': {'available_count_of_apartments': -1},
            '$pull': {'apartments': {'_id': apt['_id']}}
        })
        if apt['images']:
            for image in apt['images']:
                await self.__image_service.delete_image(image_id=image)
        return apt

    async def update_apartment(self, account, apartment_id: str,
                               apartment: UpdateApartmentSchema, images: Optional[list[UploadFile]] = None):

        images_id = await self.__save_images(images=images)
        data = {
            'filter': {'_id': ObjectId(apartment_id), 'account_id': account.id},
            'update': {
                '$set': apartment.transformed_dict,
                '$push': {'images': {'$each': images_id or []}}
            },
            'return_document': True
        }
        if (apartment := await self.__apartment_collection.find_one_and_update(**data)) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Apartment not found')
        return apartment

    async def detail_apartment(self, apartment_id: str):
        pipeline = [
            self.match(query={'_id': ObjectId(apartment_id)}),
            self.add_fields(new_name='apt_id', operator='toString', old_name='_id'),
            self.lookup('review', 'apartment_id', 'apt_id', 'reviews')
        ]
        if apt := (await self.__apartment_collection.aggregate(pipeline=pipeline).to_list(length=1))[0]:
            return apt

    async def __get_common_pipeline(self, skip: int, limit: int, _filter: dict):
        return [
            self.match(_filter),
            self.add_fields('apt_id', 'toString', '_id'),
            self.lookup('review', 'apartment_id', 'apt_id', 'reviews'),
            self.skip(skip),
            self.limit(limit),
            self.sort(created=-1),
        ]

    async def all_available_apartments(self, hotel_id: str, query_data: ApartmentQuerySchema,
                                       skip: int, limit: int):
        query = ApartmentQueryService().prepare_query_data(data=query_data)
        query.update({'hotel_id': hotel_id})
        pipeline = await self.__get_common_pipeline(skip=skip, limit=limit, _filter=query)
        return [apt async for apt in self.__apartment_collection.aggregate(pipeline=pipeline)]

    async def search(self, search_data: SearchApartmentSchema, skip: int, limit: int):
        pipeline = await self.__get_common_pipeline(skip, limit, self.search_text(search_data.search_query))
        cursor = self.__apartment_collection.aggregate(pipeline=pipeline)
        return [apt async for apt in cursor]

    async def delete_image(self, image_id: str, account):
        async with await client.start_session() as session:
            async with session.start_transaction():
                await self.__image_service.delete_image(image_id=image_id)
                filter_data = {'filter': {'account_id': account.id, 'images': {'$in': [ObjectId(image_id)]}}}
                apartment = await self.__apartment_collection.find_one(**filter_data)
                updated_data = {
                    'filter': {'_id': apartment['_id']},
                    'update': {'$pull': {'images': ObjectId(image_id)}}
                }
                await self.__apartment_collection.update_one(**updated_data)
