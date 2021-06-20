from schematics.models import Model
from schematics import types


class RentalPropertyRaw(Model):
    """Represents a rental house raw data."""

    zameen_id = types.StringType()
    title = types.StringType()
    description = types.StringType()
    price = types.StringType()
    area = types.StringType()
    beds = types.StringType()
    bathrooms = types.StringType()
    area = types.StringType()
    link = types.StringType()
    date_added_on_zameen = types.StringType()
    date_updated_on_zameen = types.StringType()
    sq_yards = types.StringType()
