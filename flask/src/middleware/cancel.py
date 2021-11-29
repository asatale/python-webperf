from functools import wraps
from flask import abort
from config import cfg
import random


def cancel_middleware(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if cfg.cancel and cfg.cprob > 0:
            rand = random.randint(0, 100)
            if rand <= cfg.cprob:
                abort(503)
        return f(*args, **kwargs)
    return decorated_function
