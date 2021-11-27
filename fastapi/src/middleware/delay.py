import asyncio
import random

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from config import cfg
from log import logger


SECOND_TO_MILLISECOND = 0.001


class DelayMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(
            self,
            request: Request,
            call_next: RequestResponseEndpoint) -> Response:
        if cfg.delay > 0 and cfg.dprob > 0:
            rand = random.randint(0, 100)
            if rand <= cfg.dprob:
                await asyncio.sleep(cfg.delay * SECOND_TO_MILLISECOND)
        return await call_next(request)
