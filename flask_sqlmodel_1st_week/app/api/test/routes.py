from flask import Blueprint
from app.api.users.utils import response

tests = Blueprint('tests', __name__)


# Test route
@tests.route('/test', methods=['GET'])
def test():
    return response(success=True, data={"message": "Hello, World! from tests route"}, status_code=200)

