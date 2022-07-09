from bson import ObjectId
from fastapi import UploadFile, status
from common_exceptions import raise_exception
from gridfs import NoFile
from motor.motor_asyncio import AsyncIOMotorGridFSBucket

from .image_service_interface import ImageServiceInterface


def image_not_found_decorator(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NoFile:
            raise_exception(status.HTTP_404_NOT_FOUND, 'Image not found')

    return wrapper


class ImageService(ImageServiceInterface):
    def __init__(self, database):
        self.__grid_fs = AsyncIOMotorGridFSBucket(database)

    @staticmethod
    async def __get_chunks(grid):
        while True:
            chunk = await grid.readchunk()
            if not chunk:
                break
            yield chunk

    @image_not_found_decorator
    async def read_image(self, image_id: str):
        grid_out = await self.__grid_fs.open_download_stream(
            file_id=ObjectId(image_id))
        return self.__get_chunks(grid=grid_out)

    @image_not_found_decorator
    async def write_image(self, image: UploadFile, image_name: str) -> ObjectId:
        return await self.__grid_fs.upload_from_stream(
            filename=image_name, source=await image.read())

    @image_not_found_decorator
    async def delete_image(self, image_id: str):
        await self.__grid_fs.delete(file_id=ObjectId(image_id))
