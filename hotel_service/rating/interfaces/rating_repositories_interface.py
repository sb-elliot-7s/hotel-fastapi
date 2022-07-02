from abc import ABC, abstractmethod

from ..schemas import RateApartmentSchema


class RatingRepositoriesInterface(ABC):
    @abstractmethod
    async def rate_apartment(self, apartment_id: str, account,
                             rate_apartment_data: RateApartmentSchema):
        pass

    @abstractmethod
    async def change_rating(self, rating_id: str, account,
                            rate_apartment_data: RateApartmentSchema):
        pass
