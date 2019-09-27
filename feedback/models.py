from datetime import datetime
from feedback import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Registration.query.get(user_id)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(20), unique=True, nullable=False)
    dealer = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.String, nullable=False)
    comments = db.Column(db.String(120),nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, customer, dealer, rating, comments, date=None):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments
        # self.date = date

    def __repr__(self):
        return f"Feedback('{self.customer}, {self.dealer}, {self.rating}, {self.comments}')"

class Registration(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.fullname}, {self.email})"