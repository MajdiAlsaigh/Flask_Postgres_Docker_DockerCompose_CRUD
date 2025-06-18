from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
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
with app.app_context():
    db.create_all()


# Creat a test route
@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({"message": "Test successful route"}), 200)


# Creat a user
@app.route('/users', methods=['POST'])
def create_user():
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


# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
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
