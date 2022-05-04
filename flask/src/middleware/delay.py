from functools import wraps
from config import cfg
import time
import random


MILLISECOND_IN_SECOND = 1000


def delay_middleware(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if cfg.delay > 0 and cfg.dprob > 0:
            rand = random.randint(0, 100)
            if rand <= cfg.dprob:
                time.sleep(cfg.delay/MILLISECOND_IN_SECOND)
        return f(*args, **kwargs)
    return decorated_function
