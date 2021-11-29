import asyncio
import random

from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from config import cfg


class CancelMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(
            self,
            request: Request,
            call_next: RequestResponseEndpoint) -> Response:
        if cfg.cancel and cfg.cprob > 0:
            rand = random.randint(0, 100)
            if rand <= cfg.cprob:
                return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        return await call_next(request)
