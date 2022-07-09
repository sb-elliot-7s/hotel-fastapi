from abc import ABC, abstractmethod
from typing import Optional

from fastapi import UploadFile

from ..apartment_schemas import CreateApartmentSchema, ApartmentQuerySchema, \
    UpdateApartmentSchema, SearchApartmentSchema


class ApartmentRepositoriesInterface(ABC):
    @abstractmethod
    async def create_apartment(self, account, apartment: CreateApartmentSchema,
                               images: Optional[list[UploadFile]] = None):
        pass

    @abstractmethod
    async def remove_apartment(self, account, apartment_id: str): pass

    @abstractmethod
    async def update_apartment(self, account, apartment_id: str,
                               apartment: UpdateApartmentSchema,
                               images: Optional[list[UploadFile]] = None):
        pass

    @abstractmethod
    async def detail_apartment(self, apartment_id: str): pass

    @abstractmethod
    async def all_available_apartments(self, hotel_id: str,
                                       query_data: ApartmentQuerySchema,
                                       limit: int, skip: int):
        pass

    @abstractmethod
    async def search(self, search_data: SearchApartmentSchema, skip: int,
                     limit: int):
        pass

    @abstractmethod
    async def delete_image(self, image_id: str, account):
        pass
