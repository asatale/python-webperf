import socket
from aioprometheus.service import Service
from aioprometheus import Counter
from log import logger


class PrometheusServer:
    def __init__(self, listen_addr: str):
        self._addr, self._port = listen_addr.split(":")
        self._server = Service()

    async def start(self):
        logger.info("Starting PrometheusServer")
        try:
            await self._server.start(addr=self._addr, port=self._port)
        except asyncio.CancelledError:
            logger.info("Received cancellederror exception")
            await self.stop()
        
    async def stop(self):
        logger.info("Stopping PrometheusServer")
        await self._server.stop()


const_label = {
    "host": socket.gethostname(),
    "app": "Python Asyncio GRPCServer"
}

total_request_metric = Counter(
    "python_server_total_requests",
    "Total number of requests received",
    const_labels=const_label
)
