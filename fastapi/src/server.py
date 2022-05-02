import asyncio
import uvicorn
import multiprocessing
from fastapi import FastAPI
from middleware import DelayMiddleware, CancelMiddleware
from api import EchoRouter
from config import cfg
from log import logger
from prometheus import PrometheusServer



def _num_workers():
    return (multiprocessing.cpu_count()* 2) + 1

def get_uvicorn_config(app, addr, port):
    return uvicorn.Config(
        app=app,
        host=addr,
        port=int(port),
        log_level="warning",
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
        limit_concurrency=10000,
        workers=_num_workers(),
        loop=loop
    )


def create_app():
    app = FastAPI()
    app.include_router(EchoRouter)
    app.add_middleware(DelayMiddleware)
    app.add_middleware(CancelMiddleware)
    return app

async def main(loop):
    addr, port = cfg.addr.split(":")
    app = create_app()
    config = get_uvicorn_config(app, addr, port)
    uvicorn_server = uvicorn.Server(config)
    prometheus_server = PrometheusServer(cfg.prometheus)

    logger.info("Starting Server")
    await asyncio.gather(
        uvicorn_server.serve(),
        prometheus_server.start()
    )
    logger.info("Stopping Server")
    

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.run(main(loop))
    
