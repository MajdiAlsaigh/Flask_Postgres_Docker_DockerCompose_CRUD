from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
from sqlalchemy.exc import SQLAlchemyError

from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object
db = SQLAlchemy()
db.init_app(app)


# Function to create a standardized response
def response(success=True, data=None, error=None, status_code=200):
    body = {"success": success}

    if success:
        if data is not None:
            body["data"] = data
    else:
        body["error"] = error or "Unknown error"

    return make_response(jsonify(body), status_code)


# Define the Users model
class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }


# Create the database and tables
=======
from os import environ

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URI')
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}  # Fixed self.id


# Move db.create_all() inside an application context
>>>>>>> 4660c4ecedfa9aeada716089af7021279595ffa8
with app.app_context():
    db.create_all()


# Creat a test route
@app.route('/test', methods=['GET'])
def test():
<<<<<<< HEAD
    return make_response(jsonify({"message": "Hello, World!"}), 200)
=======
    return make_response(jsonify({"message": "Test successful route"}), 200)
>>>>>>> 4660c4ecedfa9aeada716089af7021279595ffa8


# Creat a user
@app.route('/users', methods=['POST'])
def create_user():
<<<<<<< HEAD
    data = request.get_json()

    if not data or not data.get("username") or not data.get("email"):
        return response(
            success=False,
            error="Invalid input. 'username' and 'email' are required.",
            status_code=400
        )

    try:
        new_user = Users(
            username=data["username"],
            email=data["email"]
        )
        db.session.add(new_user)
        db.session.commit()

        return response(
            success=True,
            data=new_user.json(),
            status_code=201
        )

    except SQLAlchemyError:
        db.session.rollback()
        return response(
            success=False,
            error="Database error while creating the user.",
            status_code=500
        )

    except Exception:
        return response(
            success=False,
            error="Unexpected error occurred while creating the user.",
            status_code=500
        )
=======
    try:
        data = request.get_json()
        if not data or not data.get('username') or not data.get('email'):
            return make_response(jsonify({"error": "Invalid input"}), 400)

        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()

        return make_response(jsonify({"message": "User successful created"}), 201)
    except Exception as e:
        return make_response(jsonify({"message": "Error creating user"}), 500)
>>>>>>> 4660c4ecedfa9aeada716089af7021279595ffa8


# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
<<<<<<< HEAD
        users = Users.query.all()
        result = [user.json() for user in users]

        return response(
            success=True,
            data={
                "meta": {"count": len(result)},
                "users": result
            },
            status_code=200
        )

    except SQLAlchemyError:
        db.session.rollback()
        return response(
            success=False,
            error="Database error while retrieving users.",
            status_code=500
        )

    except Exception:
        return response(
            success=False,
            error="Unexpected error occurred while retrieving users.",
            status_code=500
        )


# Get a user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = Users.query.get(user_id)

        if not user:
            return response(
                success=False,
                error=f"User with id {user_id} not found.",
                status_code=404
            )

        return response(
            success=True,
            data=user.json(),
            status_code=200
        )

    except SQLAlchemyError:
        db.session.rollback()
        return response(
            success=False,
            error="Database error while retrieving the user.",
            status_code=500
        )

    except Exception:
        return response(
            success=False,
            error="Unexpected error occurred while retrieving the user.",
            status_code=500
        )


# Update a user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    if not data:
        return response(
            success=False,
            error="No input provided.",
            status_code=400
        )

    try:
        user = Users.query.get(user_id)
        if not user:
            return response(
                success=False,
                error=f"User with id {user_id} not found.",
                status_code=404
            )

        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        db.session.commit()

        return response(
            success=True,
            data=user.json(),
            status_code=200
        )

    except SQLAlchemyError:
        db.session.rollback()
        return response(
            success=False,
            error="Database error while updating the user.",
            status_code=500
        )

    except Exception:
        return response(
            success=False,
            error="Unexpected error occurred while updating the user.",
            status_code=500
        )


# Delete a user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = Users.query.get(user_id)
        if not user:
            return response(
                success=False,
                error=f"User with id {user_id} not found.",
                status_code=404
            )

        db.session.delete(user)
        db.session.commit()

        return response(
            success=True,
            data={"message": f"User {user_id} deleted."},
            status_code=200
        )

    except SQLAlchemyError:
        db.session.rollback()
        return response(
            success=False,
            error="Database error while deleting the user.",
            status_code=500
        )

    except Exception:
        return response(
            success=False,
            error="Unexpected error occurred while deleting the user.",
            status_code=500
        )

# Run the Flask application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
=======
        users = User.query.all()
        return make_response(jsonify([user.json() for user in users]), 200)
    except Exception as e:
        return make_response(jsonify({"message": "Error getting users"}), 500)


# Get a user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify(user.json()), 200)
        return make_response(jsonify({"message": "User not found"}), 404)
    except Exception as e:
        return make_response(jsonify({"message": "Error getting user"}), 500)


# Update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)

        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "No data provided"}), 400)

        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']

        db.session.commit()
        return make_response(jsonify({"message": "User updated successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"message": "Error updating user"}), 500)


# Delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)

        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message": "User deleted successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"message": "Error deleting user"}), 500)
>>>>>>> 4660c4ecedfa9aeada716089af7021279595ffa8
