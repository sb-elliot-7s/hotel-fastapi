from database import hotel_database

apartment_collection = hotel_database.apartment


async def get_apartment_collection(): yield apartment_collection
