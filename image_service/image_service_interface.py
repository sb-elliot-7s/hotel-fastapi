from abc import ABC, abstractmethod

from bson import ObjectId
from fastapi import UploadFile


class ImageServiceInterface(ABC):
    @abstractmethod
    async def read_image(self, image_id: str): pass

    @abstractmethod
    async def write_image(
            self, image: UploadFile, image_name: str) -> ObjectId:
        pass

    @abstractmethod
    async def delete_image(self, image_id: str): pass
