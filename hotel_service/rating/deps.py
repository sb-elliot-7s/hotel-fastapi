from database import hotel_database

rating_collection = hotel_database.rating


async def get_rating_collection(): yield rating_collection
