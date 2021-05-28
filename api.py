"""Api fron frontend"""
# not implemented yet
from flask import Blueprint

api = Blueprint('urls2', __name__, url_prefix="api")


@api.route('/')
def index():
    return 'api is not implemented yet'
