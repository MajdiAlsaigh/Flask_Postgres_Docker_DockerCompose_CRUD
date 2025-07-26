from flask import Blueprint, render_template
from app.api.users.utils import response

tests = Blueprint('tests', __name__)


# Test route
@tests.route('/test', methods=['GET'])
def test():
    return render_template('test.html')


