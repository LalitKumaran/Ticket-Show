from . import db
import datetime

class User(db.Model):
    user_id = db.Column(db.String(150), primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(150), unique=True)
    city = db.Column(db.String(150))
    password = db.Column(db.String(150))
    user_type = db.Column(db.String(150))

class Show(db.Model):
    show_id = db.Column(db.String(150), primary_key=True)
    showname = db.Column(db.String(150))
    rating = db.Column(db.Integer)
    date = db.Column(db.String(150),nullable=False)
    time = db.Column(db.String(150),nullable=False)
    price = db.Column(db.Integer)
    tag = db.Column(db.String(150))
    category = db.Column(db.String(150),nullable=False)
    cast = db.Column(db.String(200))
    lang = db.Column(db.String(150),nullable=False)
    duration = db.Column(db.String(150))
    venue = db.Column(db.String(150),nullable=False)
    poster = db.Column(db.Text, nullable=False)
    seats = db.Column(db.Integer)

class Venue(db.Model):
    venue_id = db.Column(db.String(150), primary_key=True)
    venuename = db.Column(db.String(150))
    location = db.Column(db.String(150))
    capacity = db.Column(db.Integer)
    type = db.Column(db.String(150),nullable=False)
    image = db.Column(db.Text, nullable=False)

class Booking(db.Model):
    booking_id = db.Column(db.String(150), primary_key=True)
    seatcount = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.String(150), db.ForeignKey('user.user_id'))
    show_id = db.Column(db.String(150), db.ForeignKey('show.show_id'))
