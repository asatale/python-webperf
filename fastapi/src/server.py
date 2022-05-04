import asyncio
import multiprocessing
import gunicorn.app.base
from fastapi import FastAPI
from middleware import DelayMiddleware, CancelMiddleware
from api import EchoRouter
from config import cfg
from log import logger
from prometheus import PrometheusServer

def _num_workers():
    return (multiprocessing.cpu_count() * 2) + 1

# def get_uvicorn_config(app, addr, port):
#     return uvicorn.Config(
#         app=app,
#         host=addr,
#         port=int(port),
#         log_level="warning",
#         log_config={
#             "version": 1,
#             "formatters": {
#                 "default": {
#                     "()": "uvicorn.logging.AccessFormatter",
#                     "fmt": '[%(asctime)s] [%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
#                     "use_colors": True,
#                 },
#                 "access": {
#                     "()": "uvicorn.logging.AccessFormatter",
#                     "fmt": '[%(asctime)s] [%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
#                     "use_colors": True,
#                 },
#             },
#         },
#         limit_concurrency=10000,
#         loop=loop
#     )


class Server(gunicorn.app.base.BaseApplication):

    def __init__(self, app: FastAPI, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def create_app():
    app = FastAPI()
    app.include_router(EchoRouter)
    app.add_middleware(DelayMiddleware)
    app.add_middleware(CancelMiddleware)
    return app

def main():
    options = {
        "bind": cfg.addr,
        "workers": _num_workers(),
        "worker_class": "worker.CustomUvicornWorker",
    }
    Server(create_app(), options).run()
    

if __name__ == "__main__":
    main()
    
