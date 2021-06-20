from typing import Text
from schemas.job import Job

class BaseCrawler:
    """Interface of a crawler."""

    BASE_URL = "https://www.zameen.com"
    GOOGLE_REFERER_URL = "https://www.google.com/"

    def process_job(self, job: Job):
        """Processes a crawl job.
        
        Args:
            job: Job to process.
        """
        raise NotImplementedError
