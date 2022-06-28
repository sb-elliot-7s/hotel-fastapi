from database import hotel_database

booking_collection = hotel_database.booking


async def get_booking_collection(): yield booking_collection
