from flask import Blueprint
from middleware.cancel import cancel_middleware
from middleware.delay import delay_middleware

hello_blueprint = Blueprint('hello', __name__)


@hello_blueprint.route('/')
@cancel_middleware
@delay_middleware
def say_hello():
    return "{result: Ok, message: Success}"
