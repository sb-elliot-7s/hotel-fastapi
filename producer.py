import asyncio
from aiokafka import AIOKafkaProducer

loop = asyncio.get_event_loop()
producer = AIOKafkaProducer(bootstrap_servers='localhost:9092', loop=loop)
