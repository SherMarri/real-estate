import json
import os
import random
from datetime import datetime
from typing import Any, Dict, List, Optional, Text

from bs4 import BeautifulSoup
from bs4.element import Tag
from schemas.area import Area
from schemas.job import Job
from schemas.rental_house_raw import RentalPropertyRaw
from utils.curl_util import exec_curl
from utils.rate_limit import rate_limit


from crawlers.base_crawler import BaseCrawler


class RentalAreaPropertyCrawler(BaseCrawler):
    """Crawlers an area's properties. Does not crawl a single property, only generates a list of properties."""

    def __init__(self) -> None:
        self._job: Optional[Job] = None
        self._areas: Optional[List[Area]] = None
        self._current_area: Optional[Area] = None
        self._rental_houses: Dict[Text,RentalPropertyRaw] = {}
        self._next_url: Optional[Text] = None

    def process_job(self, job: Job):
        """Processes a crawl job.
        
        Args:
            job: Job to process.
        """
        self._job = job
        self._areas = self._load_areas(job)
        self._current_area = self._choose_uncrawled_area()
        self._rental_houses = {}
        self._crawl_area_properties()
    
    def _choose_uncrawled_area(self) -> Area:
        """Returns a random uncrawled leaf area in a city."""
        if not self._areas:
            raise ValueError("_areas cannot be None.")
        # Load city areas.
        uncrawled_areas = [area for area in self._areas if area.date_last_crawled is None and area.is_leaf]
        index = random.randint(0, len(uncrawled_areas) - 1)
        return uncrawled_areas[index]
    
    def _crawl_area_properties(self):
        """Crawls properties in a leaf area."""
        if not self._current_area:
            raise ValueError("_current_area cannot be None.")
        
        area = self._current_area
        referer_url = self._generate_referer_url(area)
        try:
            print(f"Crawling properties for {area.name}")
            self._crawl_pages(area.url, referer_url)
        except Exception as e:
            print(str(e))
        
        self._save_results()
    
    def _generate_curl_command(self, url: Text, referer_url: Optional[Text] = None) -> Text:
        """Generates a curl command for a url.

        Args:
            url: URL to crawl.
            referer_url: Referer url.

        Returns:
            A curl command.
        """
        referer = ""
        if referer_url:
            referer = "-H 'Referer: %s'" % referer_url

        command = (
            """curl '%%ZAMEEN_URL%%' -S -s \
            -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36' \
            -H 'Accept: */*' \
            -H 'Accept-Language: en-US,en;q=0.5' \
            --compressed \
            -H 'Connection: keep-alive' \
            %%REFERER%% \
            -H 'TE: Trailers'
            """
            .replace("%%ZAMEEN_URL%%", url)
            .replace("%%REFERER%%", referer)
        )
        return command
    
    def _generate_referer_url(self, area: Area) -> Optional[Text]:
        """Generates a referer url for an area.

        Args:
            area: Area to generate referer url for.
        
        Returns:
            Referer url if parent_area exists.
        """
        if not self._areas:
            raise ValueError("_areas cannot be None.")

        parent_areas: List[Area] = [ar for ar in self._areas if ar.name == area.parent_area]  # Should be at least one.
        if len(parent_areas) == 0:
            return "http://www.google.com"
        else:
            return parent_areas[0].url
    
    def _load_areas(self, job: Job) -> List[Area]:
        """Returns a list of areas for the job.

        Args:
            job: Job to return areas for.
        
        Returns:
            A list of Area objects.
        """
        with open(f"data/areas/{job.city}_rental_areas.json", "r") as file:
            data: List[Any] = json.load(file)
        
        areas = [Area(area) for area in data]
        return areas
    
    @rate_limit
    def _crawl_pages(self, url: Text, referer_url: Text):
        """Crawl pages starting from provided url.

        Args:
            url: Url to crawl.
            referer_url: Referer url to use.
        """
        if not self._current_area:
            raise ValueError("_current_area cannot be None.")

        area = self._current_area
        command = self._generate_curl_command(url, referer_url)
        response_body, status_code = exec_curl(command)

        if status_code != 200:
            raise RuntimeError(f"Failed to process area: {area.name}")
        
        if self._is_captcha(response_body):
            raise RuntimeError(f"Captcah while processing area: {area.name}")
        
        self._parse_rental_houses(response_body)
        self._parse_next_url(response_body)

        if self._next_url:
            self._crawl_pages(self._next_url, url)
    
    def _is_captcha(self, response_body: Text) -> bool:
        """Returns True if body has captcha.

        Args:
            response_body: Response body to check captcha for.
        
        Returns:
            True if body has captcha.
        """
        # TODO
        return False
    
    def _parse_rental_houses(self, response_body: Text):
        """Parses response for rental houses. Adds unique properties to rental houses list.

        Args:
            response_body: Response body to parse.
        """
        soup = BeautifulSoup(response_body, "html.parser")
        property_tags: List[Tag] = soup.find_all("li", {"aria-label": "Listing", "role": "article"})
        for tag in property_tags:
            house = self._parse_property_tag(tag)
            if not house.zameen_id in self._rental_houses:  # If unique
                self._rental_houses[house.zameen_id] = house
    
    def _parse_property_tag(self, tag: Tag) -> RentalPropertyRaw:
        """Parses a tag and returns a RentalPropertyRaw object.

        Args:
            tag: HTML tag.
        
        Returns:
            RentalPropertyRaw object populated using tag.
        """
        property = RentalPropertyRaw()
        link_tag = tag.find("a", {"aria-label": "Listing link"})
        property.title = link_tag["title"]
        property.link = link_tag["href"]
        property.zameen_id = property.link.split("-")[-3]
        price_tag: Tag = tag.find("span", {"aria-label": "Price"})
        property.price = getattr(price_tag, "text", None)
        location_tag: Tag = tag.find("div", {"aria-label": "Location"})
        property.area = getattr(location_tag, "text", None)
        beds_tag: Tag = tag.find("span", {"aria-label": "Beds"})
        property.beds = getattr(beds_tag, "text", None)
        baths_tag: Tag = tag.find("span", {"aria-label": "Baths"})
        property.bathrooms = getattr(baths_tag, "text", None)
        sq_yards_tag: Tag = tag.find("span", {"aria-label": "Area"})
        property.sq_yards = getattr(sq_yards_tag, "text", None)
        creation_date_tag: Tag = tag.find("span", {"aria-label": "Listing creation date"})
        property.date_added_on_zameen = getattr(creation_date_tag, "text", None)
        updated_date_tag: Tag = tag.find("span", {"aria-label": "Listing updated date"})
        property.date_updated_on_zameen = getattr(updated_date_tag, "text", None)
        return property
    
    
    def _parse_next_url(self, response_body):
        """Parses response_body to check if next_url exists.
        If exists, sets _next_url property of the crawler object

        Args:
            response_body: Response HTML to check.
        """
        soup = BeautifulSoup(response_body, "html.parser")
        next_tag: Tag = soup.find("a", {"title": "Next"})
        if next_tag:
            endpoint = next_tag["href"]
            self._next_url = f'{self.BASE_URL}{endpoint}'
        else:
            self._next_url = None
    
    def _save_results(self):
        """Saves the parsed properties to a json file."""
        properties: List[RentalPropertyRaw] = self._rental_houses.values()
        if len(self._rental_houses) == 0:
            return
        
        data = {
            "area": self._current_area.name,
            "city": self._job.city,
            "date_crawled": str(datetime.utcnow()),
            "total": len(self._rental_houses),
            "properties": [prop.to_primitive() for prop in properties]
        }

        file_path = f"data/rentals/{self._job.city}/{self._current_area.name}.json"
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_path, "w") as file:
            json.dump(data, file)
        
        self._update_area_crawl_date()
    
    def _update_area_crawl_date(self):
        """Updates the crawl date of the active area."""
        self._current_area.date_last_crawled = datetime.utcnow()
        data = [area.to_primitive() for area in self._areas]
        with open(f"data/areas/{self._job.city}_rental_areas.json", "w") as file:
            json.dump(data, file)
