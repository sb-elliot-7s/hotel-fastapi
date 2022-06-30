from .interfaces.review__repositories_interface import ReviewRepositoriesInterface
from .review_schemas import CreateReviewSchema


class ReviewServices:
    def __init__(self, repository: ReviewRepositoriesInterface):
        self.__repository = repository

    async def write_review(self, apartment_id: str, account, review: CreateReviewSchema):
        return await self.__repository \
            .write_review(apartment_id=apartment_id, account=account, review=review)

    async def remove_review(self, review_id: str, account):
        return await self.__repository \
            .remove_review(review_id=review_id, account=account)

    async def update_review(self, review_id: str, account, review: CreateReviewSchema):
        return await self.__repository \
            .update_review(review_id=review_id, account=account, review=review)

    async def get_reviews(self, apartment_id: str, limit: int, skip: int):
        return await self.__repository \
            .get_reviews(apartment_id=apartment_id, limit=limit, skip=skip)
