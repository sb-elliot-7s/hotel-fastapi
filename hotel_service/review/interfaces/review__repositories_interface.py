from abc import ABC, abstractmethod
from ..review_schemas import CreateReviewSchema


class ReviewRepositoriesInterface(ABC):
    @abstractmethod
    async def write_review(self, apartment_id: str, account, review: CreateReviewSchema): pass

    @abstractmethod
    async def remove_review(self, review_id: str, account): pass

    @abstractmethod
    async def update_review(self, review_id: str, account, review: CreateReviewSchema): pass

    @abstractmethod
    async def get_reviews(self, apartment_id: str, limit: int, skip: int): pass
