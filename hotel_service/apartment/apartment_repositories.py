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
from common_aggregation_mixin import AggregationMixin
from image_service.image_service_interface import ImageServiceInterface


class ApartmentRepositories(AggregationMixin, ApartmentRepositoriesInterface):
    def __init__(self, apartment_collection, hotel_collection, image_service: ImageServiceInterface):
        self.__hotel_collection = hotel_collection
        self.__image_service = image_service
        self.__apartment_collection = apartment_collection

    async def __get_apartment(self, apartment_id: str):
        if (apartment := await self.__apartment_collection
                .find_one(self.filter_apartment(_id=ObjectId(apartment_id)))) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Apartment not found')
        return apartment

    async def __update_apartment_after_images_saved(self, apartment_id: str, images_id: list[ObjectId]):
        return await self.__apartment_collection.find_one_and_update(
            self.filter_apartment(_id=ObjectId(apartment_id)),
            self.push_items_to_array(array_name='images', items=images_id, default=[]),
            return_document=True)

    async def __save_images(self, images: Optional[list[UploadFile]]):
        if images:
            return [await self.__image_service.write_image(image, image.filename) for image in images]

    async def __update_hotel(self, apartment, hotel_id: str, account_id: str):
        _filter = self.filter_apartment(
            _id=ObjectId(hotel_id), account_id=account_id,
            **self.expr_(condition=self.compare_values(
                operator='lt', left_value={'$size': '$apartments'}, right_value='$count_of_apartments')))
        if (_ := await self.__hotel_collection.find_one_and_update(_filter, update={
            **self.inc_value(available_count_of_apartments=1),
            **self.push_item_to_array(apartments=apartment)
        }, return_document=True)) is None:
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
        async with await client.start_session() as session:
            async with session.start_transaction():
                apt = await self.__create_apartment(account=account, apartment=apartment, images=images)
                await self.__update_hotel(apartment=apt, hotel_id=apartment.hotel_id, account_id=account.id)
                return apt

    async def remove_apartment(self, account, apartment_id: str):
        async with await client.start_session() as session:
            async with session.start_transaction():
                apt_filter = self.filter_apartment(_id=ObjectId(apartment_id), account_id=account.id)
                if (apt := await self.__apartment_collection.find_one_and_delete(apt_filter)) is None:
                    raise_exception(status.HTTP_404_NOT_FOUND, 'Apartment not found')
                await self.__hotel_collection.update_one(
                    filter=self.filter_apartment(_id=ObjectId(apt['hotel_id'])),
                    update={
                        **self.inc_value(available_count_of_apartments=-1),
                        **self.pull_item(apartments={'_id': apt['_id']})
                    }
                )
                if images := apt['images']:
                    for image in images:
                        await self.__image_service.delete_image(image_id=image)
                return apt

    async def update_apartment(self, account, apartment_id: str,
                               apartment: UpdateApartmentSchema, images: Optional[list[UploadFile]] = None):
        images_id = await self.__save_images(images=images)
        if (apartment := await self.__apartment_collection.find_one_and_update(
                filter=self.filter_apartment(_id=ObjectId(apartment_id), account_id=account.id),
                update={
                    **self.set_document(document=apartment.transformed_dict),
                    **self.push_items_to_array(array_name='images', items=images_id, default=[])
                }, return_document=True)) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Apartment not found')
        return apartment

    async def detail_apartment(self, apartment_id: str):
        pipeline = await self.get_pipeline_for_detail_apartment(apartment_id=apartment_id)
        if apt := (await self.__apartment_collection.aggregate(pipeline=pipeline).to_list(length=1))[0]:
            return apt

    async def all_available_apartments(self, hotel_id: str, query_data: ApartmentQuerySchema,
                                       skip: int, limit: int):
        query = ApartmentQueryService().prepare_query_data(data=query_data)
        query.update({'hotel_id': hotel_id})
        pipeline = await self.get_common_pipeline_for_find_apartments(skip=skip, limit=limit, _filter=query)
        return [apt async for apt in self.__apartment_collection.aggregate(pipeline=pipeline)]

    async def search(self, search_data: SearchApartmentSchema, skip: int, limit: int):
        query = self.search_text(search_data.search_query)
        query.update({'is_booked': False})
        pipeline = await self.get_common_pipeline_for_find_apartments(skip=skip, limit=limit, _filter=query)
        return [apt async for apt in self.__apartment_collection.aggregate(pipeline=pipeline)]

    async def delete_image(self, image_id: str, account):
        async with await client.start_session() as session:
            async with session.start_transaction():
                await self.__image_service.delete_image(image_id=image_id)
                apartment = await self.__apartment_collection.find_one(
                    self.filter_apartment(account_id=account.id, images=self.check_in([ObjectId(image_id)])))
                await self.__apartment_collection \
                    .update_one(filter=self.filter_apartment(_id=apartment['_id']),
                                update=self.pull_item(images=ObjectId(image_id)))
