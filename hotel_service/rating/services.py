from .interfaces.rating_repositories_interface import \
    RatingRepositoriesInterface
from .schemas import RateApartmentSchema


class RatingService:
    def __init__(self, repository: RatingRepositoriesInterface):
        self.__repository = repository

    async def rate_apartment(self, account, apartment_id: str,
                             rate_data: RateApartmentSchema):
        return await self.__repository \
            .rate_apartment(account=account, apartment_id=apartment_id,
                            rate_apartment_data=rate_data)

    async def change_rating(self, rating_id: str, account,
                            rate_apartment_data: RateApartmentSchema):
        return await self.__repository \
            .change_rating(rating_id=rating_id, account=account,
                           rate_apartment_data=rate_apartment_data)
