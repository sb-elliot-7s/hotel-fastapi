from database import hotel_database

favorite_collection = hotel_database.favorite


async def get_favorite_collection(): yield favorite_collection
