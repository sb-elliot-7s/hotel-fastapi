import datetime
from bson import ObjectId
from .interfaces.review__repositories_interface import ReviewRepositoriesInterface
from .review_schemas import CreateReviewSchema
from common_exceptions import raise_exception
from fastapi import status


class ReviewRepositories(ReviewRepositoriesInterface):
    def __init__(self, review_collection):
        self._review_collection = review_collection

    async def __get_review(self, review_id: str):
        if (review := await self._review_collection.find_one(filter={'_id': ObjectId(review_id)})) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Review not found')
        return review

    async def write_review(self, apartment_id: str, account, review: CreateReviewSchema):
        document = {
            **review.dict(),
            'account_id': account.id,
            'apartment_id': apartment_id,
            'date_posted': datetime.datetime.utcnow()
        }
        result = await self._review_collection.insert_one(document=document)
        return await self.__get_review(review_id=result.inserted_id)

    async def remove_review(self, review_id: str, account):
        review_filter = {'_id': ObjectId(review_id), 'account_id': account.id}
        if (review := await self._review_collection.find_one_and_delete(filter=review_filter)) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Review not found')
        return review

    async def update_review(self, review_id: str, account, review: CreateReviewSchema):
        review_filter = {'_id': ObjectId(review_id), 'account_id': account.id}
        review_update = {'$set': {**review.dict(), 'date_updated': datetime.datetime.utcnow()}}
        if (review := await self._review_collection.find_one_and_update(
                filter=review_filter, update=review_update, return_document=True)) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Review not found')
        return review

    async def get_reviews(self, apartment_id: str, limit: int, skip: int):
        cursor = self._review_collection \
            .find({'apartment_id': apartment_id}) \
            .skip(skip) \
            .limit(limit) \
            .sort('date_posted', -1)
        return [rev async for rev in cursor]
