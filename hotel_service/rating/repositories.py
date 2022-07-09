from datetime import datetime

from bson import ObjectId
from common_aggregation_mixin import AggregationMixin
from .interfaces.rating_repositories_interface import \
    RatingRepositoriesInterface
from .schemas import RateApartmentSchema
from fastapi import status
from common_exceptions import raise_exception


class RatingRepositories(AggregationMixin, RatingRepositoriesInterface):
    def __init__(self, rating_collection, apartment_collection):
        self.__rating_collection = rating_collection
        self.__apartment_collection = apartment_collection

    async def __get_rating(self, rating_id: str):
        if not (rating := await self.__rating_collection.find_one(
                {'_id': ObjectId(rating_id)})):
            raise_exception(status.HTTP_404_NOT_FOUND, 'Rating not found')
        return rating

    async def rate_apartment(self, apartment_id: str, account,
                             rate_apartment_data: RateApartmentSchema):
        if _ := await self.__rating_collection.find_one(
                {'apartment_id': apartment_id, 'account_id': account.id}):
            raise_exception(status.HTTP_400_BAD_REQUEST,
                            "You don't rate this apartment")
        document = {
            'grade': rate_apartment_data.grade,
            'account_id': account.id,
            'apartment_id': apartment_id,
            'created': datetime.utcnow()
        }
        result = await self.__rating_collection.insert_one(document=document)
        await self.__update_apartment_avg_rating(apartment_id=apartment_id)
        return await self.__get_rating(rating_id=result.inserted_id)

    async def change_rating(self, rating_id: str, account,
                            rate_apartment_data: RateApartmentSchema):
        if (rating := await self.__rating_collection.find_one_and_update(
                filter=self.filter_objects(_id=ObjectId(rating_id),
                                           account_id=account.id),
                update=self.set_document({'updated': datetime.utcnow(),
                                          'grade': rate_apartment_data.grade}),
                return_document=True)) is None:
            raise_exception(status.HTTP_404_NOT_FOUND,
                            f'Rating {rating_id} not found')
        await self.__update_apartment_avg_rating(
            apartment_id=rating['apartment_id'])
        return rating

    async def __calculate_rating_for_apartment(self, apartment_id: str):
        pipeline = [
            self.match(query={'apartment_id': apartment_id}),
            self.group_by(_id='$apartment_id', avg_rating={'$avg': '$grade'}),
            self.project(apartment_id='$_id', avg_rating=1, _id=0)
        ]
        cursor = self.__rating_collection.aggregate(pipeline=pipeline)
        return (await cursor.to_list(length=1))[0]

    async def __update_apartment_avg_rating(self, apartment_id: str):
        rating: dict = await self.__calculate_rating_for_apartment(
            apartment_id=apartment_id)
        await self.__apartment_collection.update_one(
            {'_id': ObjectId(rating.get('apartment_id'))},
            self.set_document({'avg_rating': rating.get('avg_rating')})
        )

    async def calculate_avg_rating_for_apartments(self):
        pipeline = [
            self.group_by(_id='$apartment_id', avg_rating={'$avg': '$grade'}),
            self.project(apartment_id='$_id', avg_rating=1, _id=0)
        ]
        return [avg_rating async for avg_rating in
                self.__rating_collection.aggregate(pipeline=pipeline)]
