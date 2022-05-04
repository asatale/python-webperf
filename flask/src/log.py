import logging
import sys

stdout_handler = logging.StreamHandler(sys.stdout)

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d]: %(message)s',
    handlers=[stdout_handler])

logger = logging.getLogger("WSGIApp")
