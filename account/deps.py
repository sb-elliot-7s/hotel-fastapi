from database import hotel_database

account_collection = hotel_database.account


async def get_account_collection(): yield account_collection
