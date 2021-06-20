import json
from typing import List, Optional, Text

from bs4 import BeautifulSoup
from bs4.element import Tag
from schemas.area import Area
from schemas.job import Job
from utils.curl_util import exec_curl
from utils.rate_limit import rate_limit

from crawlers.base_crawler import BaseCrawler


class RentalAreaCrawler(BaseCrawler):
    """Crawler for retrieving areas for rentals."""

    def __init__(self) -> None:
        self._areas: List[Area] = []    

    def process_job(self, job: Job):
        """Processes a crawl job.
        
        Args:
            job: Job to process.
        """
        area = Area()
        area.name = job.city
        area.parent_area = None
        area.url = job.start_url
        area.processed = False
        self._areas.append(area)

        requests = 0
        while self._has_unprocessed_areas():
            area = self._get_area_to_process()
            try:
                self._process_area(area)
                area.processed = True
                print(f"Processed area successfully: {area.name}")
            except Exception as e:
                print(str(e))
                area.failed = True

            requests += 1
            print(f"Total requests: {requests}")
        
        self._save_results()
    
    @rate_limit
    def _process_area(self, area: Area):
        """Processes a url.

        Args:
            area: Area to crawl and process.
        """
        command = self._generate_curl_command(area.url)
        response_body, status_code = exec_curl(command)

        if status_code != 200:
            raise RuntimeError(f"Failed to process area: {area.name}")
        
        if self._is_captcha(response_body):
            raise RuntimeError(f"Captcah while processing area: {area.name}")

        areas: List[Area] = self._parse_areas(area, response_body)
        if len(areas) > 0:
            self._areas.extend(areas)
            
    def _generate_curl_command(self, url: Text) -> Text:
        """Generates a curl command for a url.

        Args:
            url: URL to crawl.

        Returns:
            A curl command.
        """
        command = (
            """curl '%%ZAMEEN_URL%%' -S -s \
            -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36' \
            -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' \
            -H 'Accept-Language: en-US,en;q=0.5' \
            --compressed \
            -H 'Connection: keep-alive'  \
            -H 'Upgrade-Insecure-Requests: 1' \
            -H 'Cache-Control: max-age=0' \
            -H 'Referer: %%REFERER%%'
            """
            .replace("%%ZAMEEN_URL%%", url)
            .replace("%%REFERER%%", self.GOOGLE_REFERER_URL)
        )
        return command

    
    def _is_captcha(self, response_body: Text) -> bool:
        """Returns true response_body has captcha.
        
        Args:
            response_body: Text -> HTML text of response.
        
        Returns:
            bool -> If response has captcha, else False.
        """
        # TODO
        return False
    
    def _parse_areas(self, area: Area, response_body: Text) -> List[Area]:
        """Parses areas in response_body and returns them.

        Args:
            area: Area to parse.
            response_body: HTML text of response.
        
        Returns:
            List of Areas in response_body.
        """
        soup = BeautifulSoup(response_body, "html.parser")
        areas: List[Area] = []
        location_links: List[Tag] = soup.find_all("div", {"aria-label": "Location links"})
        if len(location_links) == 0:  # is_leaf area
            area.is_leaf = True
            return areas
        
        link_div: Tag = location_links[0]
        area_links = link_div.find_all("a")
        for link in area_links:
            c_area = Area()
            c_area.url = f'{self.BASE_URL}{link["href"]}'
            c_area.name = link.text.split("(")[0].strip()
            c_area.parent_area = area.name
            areas.append(c_area)
        
        return areas
    
    def _has_unprocessed_areas(self) -> bool:
        """Returns true if crawler has unprocessed areas.
        
        Returns:
            bool: True if crawler has unprocessed areas, else False.
        """
        for area in self._areas:
            if not (area.processed or area.failed):
                return True
        
        return False
    
    def _get_area_to_process(self) -> Optional[Area]:
        """Returns an area to process.

        Returns:
            Area: Area to process.
        """
        for area in self._areas:
            if not (area.processed or area.failed):
                return area
        
        return None
    
    def _save_results(self):
        """Saves job results."""
        areas = [area.to_native() for area in self._areas]
        with open(f"data/areas/{self._areas[0].name}_rental_areas.json", "w") as file:
            json.dump(areas, file)
