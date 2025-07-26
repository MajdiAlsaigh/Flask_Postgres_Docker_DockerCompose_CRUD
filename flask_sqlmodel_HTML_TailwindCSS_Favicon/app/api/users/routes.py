from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.user import Users
from app.api.users.utils import response

users = Blueprint('users', __name__)


# Create a user
@users.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("email"):
        return response(False, error="Invalid input. 'username' and 'email' are required.", status_code=400)
    try:
        new_user = Users(username=data["username"], email=data["email"])
        db.session.add(new_user)
        db.session.commit()
        return response(True, data=new_user.json(), status_code=201)
    except SQLAlchemyError:
        db.session.rollback()
        return response(False, error="Database error while creating the user.", status_code=500)
    except Exception:
        return response(False, error="Unexpected error occurred while creating the user.", status_code=500)


# Get all users
@users.route('/users', methods=['GET'])
def get_users():
    try:
        users = Users.query.all()
        result = [user.json() for user in users]
        return response(True, data={"meta": {"count": len(result)}, "users": result})
    except SQLAlchemyError:
        db.session.rollback()
        return response(False, error="Database error while retrieving users.", status_code=500)
    except Exception:
        return response(False, error="Unexpected error occurred while retrieving users.", status_code=500)


# Get a user by ID
@users.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = Users.query.get(user_id)
        if not user:
            return response(False, error=f"User with id {user_id} not found.", status_code=404)
        return response(True, data=user.json())
    except SQLAlchemyError:
        db.session.rollback()
        return response(False, error="Database error while retrieving the user.", status_code=500)
    except Exception:
        return response(False, error="Unexpected error occurred while retrieving the user.", status_code=500)


# Update a user by ID
@users.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return response(False, error="No input provided.", status_code=400)
    try:
        user = Users.query.get(user_id)
        if not user:
            return response(False, error=f"User with id {user_id} not found.", status_code=404)
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        db.session.commit()
        return response(True, data=user.json())
    except SQLAlchemyError:
        db.session.rollback()
        return response(False, error="Database error while updating the user.", status_code=500)
    except Exception:
        return response(False, error="Unexpected error occurred while updating the user.", status_code=500)


# Delete a user by ID
@users.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = Users.query.get(user_id)
        if not user:
            return response(False, error=f"User with id {user_id} not found.", status_code=404)
        db.session.delete(user)
        db.session.commit()
        return response(True, data={"message": f"User {user_id} deleted."})
    except SQLAlchemyError:
        db.session.rollback()
        return response(False, error="Database error while deleting the user.", status_code=500)
    except Exception:
        return response(False, error="Unexpected error occurred while deleting the user.", status_code=500)

