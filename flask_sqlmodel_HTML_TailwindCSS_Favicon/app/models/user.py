from app import db


# Define the Users model
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}
