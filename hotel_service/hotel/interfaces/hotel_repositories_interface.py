from abc import ABC, abstractmethod

from ..hotel_schemas import CreateHotelSchema, HotelSchema, QueryHotelSchema, UpdateHotelSchema


class HotelRepositoriesInterface(ABC):

    @abstractmethod
    async def create_hotel(self, hotel: CreateHotelSchema, account) -> HotelSchema: pass

    @abstractmethod
    async def remove_hotel(self, hotel_id: str, account): pass

    @abstractmethod
    async def update_hotel(self, hotel_id: str, account, hotel: UpdateHotelSchema) -> HotelSchema: pass

    @abstractmethod
    async def show_detail_hotel(self, hotel_id: str) -> HotelSchema: pass

    @abstractmethod
    async def show_hotels(self, query_data: QueryHotelSchema,
                          limit: int = 20, skip: int = 0) -> list[HotelSchema]: pass
