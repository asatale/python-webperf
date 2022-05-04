from uvicorn.workers import UvicornWorker

class CustomUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "asyncio",
                     "http": "h11",
                     "limit_concurrency": 2096,
                     "lifespan": "off"}
