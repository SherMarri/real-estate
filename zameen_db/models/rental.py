from server.api_server import db


class Rental(db.Model):
    __tablename__ = "rentals"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String())
