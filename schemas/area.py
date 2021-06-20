from schematics.models import Model
from schematics import types


class Area(Model):
    """Represents an area."""

    name = types.StringType()
    url = types.StringType()
    is_leaf = types.BooleanType()
    parent_area = types.StringType()
    processed = types.BooleanType()
    failed = types.BooleanType()
    date_last_crawled = types.DateTimeType()
