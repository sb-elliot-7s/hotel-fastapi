import motor.motor_asyncio
from configs import get_configs

client = motor.motor_asyncio.AsyncIOMotorClient(get_configs().mongodb)

hotel_database = client.hotel_database
