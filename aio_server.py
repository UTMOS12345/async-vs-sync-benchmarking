import asyncio

from aiohttp import web


async def async_task(request):
    # Non-blocking wait unlike time.sleep(0.1)
    await asyncio.sleep(0.1)
    return web.json_response({"server": "aiohttp", "status": "done"})


app = web.Application()
app.add_routes([web.get("/test", async_task)])

if __name__ == "__main__":
    web.run_app(app, port=5001)
