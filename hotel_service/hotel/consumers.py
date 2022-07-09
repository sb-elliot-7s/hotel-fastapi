import asyncio
import json

from aiokafka import AIOKafkaConsumer
from bson import ObjectId
from .deps import hotel_collection


async def update_hotel(hotel_id: str, value: int):
    await hotel_collection.update_one(
        filter={'_id': ObjectId(hotel_id)},
        update={'$inc': {'available_count_of_apartments': value}})


async def consume_available_apt():
    consumer = AIOKafkaConsumer(
        'hotel-apt-count',
        bootstrap_servers='localhost:9092',
        group_id="hotel-apt-count-group")
    await consumer.start()
    try:
        async for msg in consumer:
            data = json.loads(msg.value)
            await update_hotel(hotel_id=data['hotel_id'],
                               value=data['available_count_of_apartments'])
    finally:
        await consumer.stop()


if __name__ == '__main__':
    asyncio.run(consume_available_apt())
