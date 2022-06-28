from database import hotel_database

hotel_collection = hotel_database.hotel


async def get_hotel_collection(): yield hotel_collection
