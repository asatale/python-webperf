import uvicorn
import multiprocessing
from fastapi import FastAPI
from middleware.delay import DelayMiddleware
from middleware.cancel import CancelMiddleware
from api.hello import app as helloApp
from config import cfg

app = FastAPI()
app.mount("/", helloApp)
app.add_middleware(DelayMiddleware)
app.add_middleware(CancelMiddleware)


def main():
    def _num_workers():
        return (multiprocessing.cpu_count() * 2) + 1

    addr, port = cfg.addr.split(":")
    uvicorn.run(
        f"{__name__}:app",
        host=addr,
        port=int(port),
        log_level="info",
        workers=_num_workers())


if __name__ == "__main__":
    main()
