import asyncio
import json
from datetime import datetime

import aio_pika
import psutil

from server.database import Database
from worker.rebuild import algorithm

QUEUE_NAME = "rebuilds"
MIN_FREE_MEMORY_MB = 15000
database = Database()

def check_memory():
    available_mb = psutil.virtual_memory().available / (1024 * 1024)
    total_mb = psutil.virtual_memory().total / (1024 * 1024)
    print(f"Free memory: {available_mb} MB. Total memory: {total_mb} MB ({(available_mb / total_mb) * 100:.2f}%)")
    return available_mb > MIN_FREE_MEMORY_MB


def process(message_body: str):
    message_body = json.loads(message_body)
    payload = message_body["payload"]
    print(f"Processing message: {message_body['id']} | model {payload['model']} | dimension {payload['dimensions']}")

    started_at = datetime.now()

    database.update_rebuild(message_body["id"], "status", "running")
    database.update_rebuild(message_body["id"], "started_at")

    file_path, iterations = algorithm(payload["g"], payload["H"], payload["model"], message_body["id"], payload["dimensions"])

    database.update_rebuild(message_body["id"], "finished_at")
    database.update_rebuild(message_body["id"], "iterations", iterations)
    database.update_rebuild(message_body["id"], "file_path", file_path)
    database.update_rebuild(message_body["id"], "status", "finished")

    print(f"Message processed: {message_body['id']} in {datetime.now() - started_at} -> {file_path}")


async def handle_message(message: aio_pika.IncomingMessage):
    while not check_memory():  # todo controlar qnt de paralelos
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
                asyncio.create_task(handle_message(message))


if __name__ == "__main__":
    print("Worker started")
    asyncio.run(consume())
