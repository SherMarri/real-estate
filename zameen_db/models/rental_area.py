from datetime import datetime
from server.api_server import db


class RentalArea(db.Model):
    """Represents a rental area."""
    
    __tablename__ = "rental_areas"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String())
    url = db.Column(db.String())
    is_leaf = db.Column(db.Boolean())
    parent_area = db.Column(db.String())
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_last_crawled = db.Column(db.DateTime)
