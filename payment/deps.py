from database import hotel_database

payment_collection = hotel_database.payment


async def get_payment_collection(): yield payment_collection
