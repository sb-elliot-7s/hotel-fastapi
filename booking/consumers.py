import json

from aiokafka import AIOKafkaConsumer
import asyncio

from bson import ObjectId

from .deps import booking_collection


async def __update_booking(booking_id: str, payment_status: str):
    await booking_collection.update_one(
        filter={'_id': ObjectId(booking_id)},
        update={'$set': {'payment_status': payment_status}}
    )


async def consume_payment_status_result():
    consumer = AIOKafkaConsumer(
        'update-booking-payment-status',
        bootstrap_servers='localhost:9092',
        group_id="booking-payment-status-group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            data = json.loads(msg.value)
            await __update_booking(
                booking_id=data['booking_id'],
                payment_status=data['payment_status'])
    finally:
        await consumer.stop()


if __name__ == '__main__':
    asyncio.run(consume_payment_status_result())
