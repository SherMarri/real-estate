from server.api_server import db


class Rental(db.Model):
    """Represents a rental property."""

    __tablename__ = "rentals"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    zameen_id = db.Column(db.String())
    title = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.Integer)
    area_name = db.Column(db.String())
    beds = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    sq_yards = db.Column(db.Integer)
    link = db.Column(db.String())
    date_added_on_zameen = db.Column(db.DateTime)
    date_updated_on_zameen = db.Column(db.DateTime)
