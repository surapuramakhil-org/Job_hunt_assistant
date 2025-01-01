from typing import List, Optional
from src.job import Job
from src.job_portals.base_job_portal import BaseJobsPage
from src.logger import logger
from web_search_engine import SearchResult


#TODO: serch engine shoun't be constants, it can be dynamic, it serach engine changes, offset will be rest, limit will be differnt
class SearchLeverJobs(BaseJobsPage):
    """
    Searches for job postings on Lever-hosted pages by querying a web
    search engine (e.g., Google, Bing, Brave) using advanced site-based
    queries. Collects relevant links and converts them into Job objects.
    """

    def __init__(self, driver, work_preferences):
        """
        :param driver: A webdriver instance (if needed for further scraping).
        :param work_preferences: A dictionary containing filters such as
                                 remote/hybrid/onsite, experience levels,
                                 job type, etc.
        """
        super().__init__(driver, work_preferences)
        self.search_engine = WebSearchEngineFactory.get_search_engine() 
        self.search_offset = 0
        self.search_limit = DEFAULT_SEARCH_LIMIT  # Or define your own constant
        self.jobs = []
        self.current_query = None


    #TODO: implement complete filters of work preferences
    def next_job_page(self, position: str, location: str, page_number: int) -> None:
        """
        Moves to the next 'page' of search results by using offset-based
        pagination for the chosen search engine. The results are stored
        internally for later processing.
        
        :param position: The role or title to search for (e.g., "Software engineer").
        :param location: The location to search in (e.g., "Germany").
        :param page_number: The page number being requested.
        """
        # Calculate offset based on page_number (which can be zero-based or one-based).
        # Here we’ll assume page_number is zero-based.
        self.search_offset = page_number * self.search_limit
        self.current_query = f"site:jobs.lever.co {position} in {location}"
        logger.info(f"Querying '{self.current_query}' with offset={self.search_offset} and limit={self.search_limit}")

        response = self.search_engine.search(
            query=self.current_query,
            offset=self.search_offset,
            limit=self.search_limit
        )
        # Store new batch of links
        self.jobs = response.results

    def job_tile_to_job(self, job_tile: SearchResult) -> Job:
        """
        Converts a single search result (title, link, snippet) to a Job object
        if it passes all blacklists and preference checks. The snippet can be
        used to detect partial location or keywords.
        
        :param job_tile: A SearchResult object with (title, link, snippet).
        :return: A fully populated Job object if acceptable, otherwise None.
        """
        title_lower = job_tile.title.lower()
        snippet_lower = job_tile.snippet.lower()
        link = job_tile.link.lower()

        # Check company blacklist
        if any(blk.lower() in link for blk in self.work_preferences.get("company_blacklist", [])):
            logger.debug(f"Skipping blacklisted company: {job_tile.link}")
            return None

        # Check title blacklist
        if any(blk.lower() in title_lower for blk in self.work_preferences.get("title_blacklist", [])):
            logger.debug(f"Skipping blacklisted title: {job_tile.title}")
            return None

        # Check location blacklist
        if any(blk.lower() in snippet_lower for blk in self.work_preferences.get("location_blacklist", [])):
            logger.debug(f"Skipping blacklisted location in snippet: {job_tile.snippet}")
            return None

        # More advanced filtering can go here based on snippet or direct scraping
        # For demonstration, we’ll keep it simple.

        job = Job(
            title=job_tile.title,
            company=self._extract_company_from_link(job_tile.link),
            location="",  # Could parse snippet or further detail
            link=job_tile.link,
            source="Lever"
        )
        return job

    def get_jobs_from_page(self, scroll=False) -> List[SearchResult]:
        """
        Collects jobs from the current set of search results, transforms
        each link into a Job object, and returns the filtered list.
        
        :param scroll: (Not used here) If controlling a browser, you might
                       scroll for dynamic pages.
        :return: A list of Job objects from the current set of results.
        """
        
        return self.jobs

    def _extract_company_from_link(self, url: str) -> str:
        """
        A helper method that attempts to parse the company name from the
        Lever link. Typically, Lever postings follow the format:
        https://jobs.lever.co/<company>/<job-id>
        
        :param url: The URL to parse.
        :return: The name of the company if parsed, otherwise empty string.
        """
        # Example: jobs.lever.co/google/123abc => company = "google"
        try:
            parts = url.split('/')
            # Because the domain could be: https://jobs.lever.co/<company>
            # We find the index of '.lever.co' then skip next part
            idx = parts.index("jobs.lever.co")
            return parts[idx+1]
        except ValueError:
            return ""

