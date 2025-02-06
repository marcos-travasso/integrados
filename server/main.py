import asyncio
import random
from datetime import datetime, timezone

from aiohttp import web
from aiohttp.abc import Request

from server.database import Database
from server.rabbit import RabbitMQClient

rabbitmq = RabbitMQClient()
database = Database()


async def create_rebuild(request: Request):
    id = f"image_{random.randint(1, 1000)}"
    received_at = datetime.now(timezone.utc).isoformat()
    data = await request.json()

    message = {
        "id": id,
        "received_at": received_at,
        "payload": data
    }

    await database.insert_rebuild(id, received_at, data)

    asyncio.create_task(rabbitmq.send_to_queue(message))

    return web.json_response(data={"id": id, "received_at": received_at})


async def get_rebuild(request: Request):
    return web.Response(text="Hello, world")


async def get_status(request: Request):
    return web.Response(text="Hello, world")


async def on_startup(app):
    await rabbitmq.connect()
    await database.connect()


async def on_cleanup(app):
    await rabbitmq.close()
    await database.close()


app = web.Application()
app.add_routes([
    web.post('/rebuild', create_rebuild),
    web.get('/rebuild/{id}', get_rebuild),
    web.get('/status', get_status)
])

app.on_startup.append(on_startup)
app.on_cleanup.append(on_cleanup)

web.run_app(app)
