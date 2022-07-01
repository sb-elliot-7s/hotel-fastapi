from database import hotel_database

apartment_collection = hotel_database.apartment

apartment_collection.create_index([('title', 'text'), ('description', 'text')])


async def get_apartment_collection(): yield apartment_collection
