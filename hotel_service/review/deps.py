from database import hotel_database

review_collection = hotel_database.review


async def get_review_collection(): yield review_collection
