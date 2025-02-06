import json

import aio_pika


class RabbitMQClient:
    def __init__(self, url="amqp://guest:guest@localhost/"):
        self.url = url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()

    async def send_to_queue(self, message: dict):
        if not self.channel:
            await self.connect()
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message).encode(), content_type="application/json"),
            routing_key="rebuilds"
        )

    async def close(self):
        if self.connection:
            await self.connection.close()
