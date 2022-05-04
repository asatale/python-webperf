from flask import Blueprint
from middleware.cancel import cancel_middleware
from middleware.delay import delay_middleware

echo_blueprint = Blueprint('echo', __name__)


@echo_blueprint.route('/echo')
@cancel_middleware
@delay_middleware
def echo():
    return "{result: Ok, message: Success}"
