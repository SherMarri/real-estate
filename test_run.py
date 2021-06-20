from schemas.job import Job
from services.crawler_service import crawler_service


# job = Job()
# job.city = "Karachi"
# job.job_type = Job.JOB_TYPE_CRAWL_RENTAL_HOUSES_AREA_PROPERTIES
job = Job()
job.city = "Karachi"
job.job_type = Job.JOB_TYPE_CRAWL_RENTAL_AREA_PROPERTIES
crawler_service.process_job(job)
