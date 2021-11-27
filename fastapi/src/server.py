import uvicorn
from fastapi import FastAPI
from middleware.delay import DelayMiddleware
from middleware.cancel import CancelMiddleware
from api.route import app as route_app
from config import cfg

if __name__ == "__main__":
    app = FastAPI()
    app.mount("/", route_app)
    app.add_middleware(DelayMiddleware)
    app.add_middleware(CancelMiddleware)
    addr, port = cfg.addr.split(":")
    uvicorn.run(app, host=addr, port=int(port), log_level="warning")
