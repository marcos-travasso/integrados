import asyncio
import aio_pika


async def consume():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("rebuilds", durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(f"Received message: {message.body.decode()}")


if __name__ == "__main__":
    print("Worker started")
    asyncio.run(consume())
