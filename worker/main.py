import asyncio

import aio_pika
import psutil

QUEUE_NAME = "rebuilds"
MIN_FREE_MEMORY_MB = 17000


def check_memory():
    available_mb = psutil.virtual_memory().available / (1024 * 1024)
    total_mb = psutil.virtual_memory().total / (1024 * 1024)
    print(f"Free memory: {available_mb} MB. Total memory: {total_mb} MB ({(available_mb/total_mb)*100:.2f}%)")
    return available_mb > MIN_FREE_MEMORY_MB


def process(message_body):
    print(f"Processing message: {message_body}")
    b = []
    for i in range(100000):
        a = []
        for j in range(100000):
            a.append(j)
        b.append(a)
    print("Processed")


async def handle_message(message: aio_pika.IncomingMessage):
    while not check_memory():
        print("Waiting for memory...")
        await asyncio.sleep(1)

    await asyncio.to_thread(process, message.body.decode())

    try:
        await message.ack()
        print("Message acknowledged.")
    except aio_pika.exceptions.MessageProcessError:
        print("Message was already acknowledged or processed.")


async def consume():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                asyncio.create_task(handle_message(message))  # Non-blocking execution


if __name__ == "__main__":
    print("Worker started")
    asyncio.run(consume())
