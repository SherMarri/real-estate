from crawlers.rental_area_property_crawler import RentalAreaPropertyCrawler
from crawlers.rental_area_crawler import RentalAreaCrawler
from crawlers.base_crawler import BaseCrawler
import glob
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Text

from schemas.job import Job


class CrawlerService:
    """Service for crawling Zameen."""

    # JOB_DIRECTORY = Path("/app/data/jobs")
    JOB_DIRECTORY = Path("/home/sher/Experiments/zameen_crawler/data/jobs")

    crawler_map: Dict[Text, BaseCrawler] = {
        Job.JOB_TYPE_CRAWL_RENTAL_AREAS: RentalAreaCrawler,
        Job.JOB_TYPE_CRAWL_RENTAL_AREA_PROPERTIES: RentalAreaPropertyCrawler,
    }

    def __init__(self) -> None:
        self._job_path: Optional[Text] = None

    def process_job(self, job: Optional[Job] = None):
        self._job_path = None
        if not job:
            job: Job = self._load_first_unprocessed_job()
        crawler: BaseCrawler = self.crawler_map[job.job_type]()
        try:
            print(f"Processing job: {job.job_type}")
            print(f"Area: {job.city}")
            crawler.process_job(job)
            self._finish_job()
        except Exception as e:
            print(str(e))
    
    def _load_first_unprocessed_job(self) -> Job:
        """Returns the first unprocessed job in /app/jobs/unprocessed/ directory
        
        Returns:
            First job found in jobs/unprocessed directory.
        
        Raises:
            RunTimeError: An error occurred while reading a job, either empty directory or invalid job schema.
        """
        unprocessed_directory: Path = self.JOB_DIRECTORY.joinpath("unprocessed")
        files = glob.glob(f"{unprocessed_directory}/*job_*.json")
        for file in files:
            if os.path.isfile(file):
                self._job_path = file
        
        if not self._job_path:
            raise RuntimeError("No job found.")
        
        with open(self._job_path, "r") as file:
            job_json: Dict[Text, Any] = json.load(file)
        
        job = Job(job_json)
        return job
    
    def _finish_job(self):
        """Moves the job file to /data/jobs/processed directory
        """
        if not self._job_path:
            return
        
        processed_job_path = self._job_path.replace("unprocessed", "processed")
        os.rename(self._job_path, processed_job_path)


crawler_service = CrawlerService()
