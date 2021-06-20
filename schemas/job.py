from schematics.models import Model
from schematics import types


class Job(Model):
    """Represents a crawler job."""

    JOB_TYPE_CRAWL_RENTAL_AREAS = "crawl_rental_areas"
    JOB_TYPE_CRAWL_RENTAL_AREA_PROPERTIES = "crawl_rental_area_properties"

    job_type = types.StringType()
    city = types.StringType()
    start_url = types.StringType()
