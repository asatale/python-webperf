import asyncio
import uvicorn
import multiprocessing
from fastapi import FastAPI
from middleware.delay import DelayMiddleware
from middleware.cancel import CancelMiddleware
from api.hello import app as helloApp
from config import cfg
from log import logger

app = FastAPI()
app.mount("/", helloApp)
app.add_middleware(DelayMiddleware)
app.add_middleware(CancelMiddleware)


def main():
    def _num_workers():
        return (multiprocessing.cpu_count() * 2) + 1

    addr, port = cfg.addr.split(":")
    loop = asyncio.new_event_loop()
    config = uvicorn.Config(
        app=app,
        host=addr,
        port=int(port),
        log_level="info",
        log_config={
            "version": 1,
            "formatters": {
                "default": {
                    "()": "uvicorn.logging.AccessFormatter",
                    "fmt": '[%(asctime)s] [%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
                    "use_colors": True,
                },
                "access": {
                    "()": "uvicorn.logging.AccessFormatter",
                    "fmt": '[%(asctime)s] [%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
                    "use_colors": True,
                },
            },
        },
        limit_concurrency=1000,
        workers=_num_workers(),
        loop=loop
    )

    server = uvicorn.Server(config)

    try:
        loop.run_until_complete(server.serve())
    except Exception as e:
        logger.error(f"Exception {e} in asyncio loop")


if __name__ == "__main__":
    main()
