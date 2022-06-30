from abc import ABC, abstractmethod
from ..apartment_schemas import CreateApartmentSchema, ApartmentQuerySchema, UpdateApartmentSchema


class ApartmentRepositoriesInterface(ABC):
    @abstractmethod
    async def create_apartment(self, account, hotel_station, apartment: CreateApartmentSchema):
        pass

    @abstractmethod
    async def remove_apartment(self, account, apartment_id: str): pass

    @abstractmethod
    async def update_apartment(self, account, apartment_id: str, apartment: UpdateApartmentSchema):
        pass

    @abstractmethod
    async def detail_apartment(self, apartment_id: str): pass

    @abstractmethod
    async def all_available_apartments(self, hotel_id: str, query_data: ApartmentQuerySchema,
                                       limit: int = 20, skip: int = 0):
        pass
