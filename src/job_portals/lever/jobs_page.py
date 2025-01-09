from typing import List, Optional
from src.job import Job
from src.job_portals.base_job_portal import BaseJobsPage
from src.logger import logger
import stringcase
from  src.services.web_search_engine import SearchQueryBuilder, SearchResult, SearchTimeRange, WebSearchEngine, WebSearchEngineFactory


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
        self.search_limit = self.search_engine.DEFAULT_SEARCH_LIMIT 
        self.jobs = []
        self.current_query = None

     
    def next_job_page(self, position: str, location: str, page_number: int) -> None:
        """
        Moves to the next 'page' of search results by using offset-based pagination.
        
        :param position: The role or title to search for (e.g., "Software Engineer").
        :param location: The location to search in (e.g., "Germany").
        :param page_number: The page number being requested.
        """
        
        # Update pagination offset
        self.search_offset = page_number * self.search_limit

        # Build a unified query using SearchQueryBuilder
        query_builder = SearchQueryBuilder.create()
        
        # Add position and location to keywords
        query_builder.add_to_keywords(position)
        query_builder.set_geolocation(location)

        # Apply blacklists (location, company, title)
        if 'location_blacklist' in self.work_preferences:
            query_builder.add_to_blacklist(self.work_preferences['location_blacklist'])
        
        if 'company_blacklist' in self.work_preferences:
            query_builder.add_to_blacklist(self.work_preferences['company_blacklist'])
        
        if 'title_blacklist' in self.work_preferences:
            query_builder.add_to_blacklist(self.work_preferences['title_blacklist'])

        # Add date range filters
        if 'date' in self.work_preferences:
            if self.work_preferences['date'].get('24_hours', False):
                query_builder.set_date_range(SearchTimeRange.LAST_24_HOURS)
            elif self.work_preferences['date'].get('week', False):
                query_builder.set_date_range(SearchTimeRange.LAST_WEEK)
            elif self.work_preferences['date'].get('month', False):
                query_builder.set_date_range(SearchTimeRange.LAST_MONTH)

        # Add job types and experience levels as whitelists
        if 'job_types' in self.work_preferences:
            job_types = [key for key, enabled in self.work_preferences['job_types'].items() if enabled]
            query_builder.add_to_whitelist(job_types)

        if 'experience_level' in self.work_preferences:
            experience_levels = [key for key, enabled in self.work_preferences['experience_level'].items() if enabled]
            query_builder.add_to_whitelist(experience_levels)

        # whitelist as per work_preferences is not same as whitelist in search engine, workpreferences whitelist forces all words to be present in search result
        if 'keywords_whitelist' in self.work_preferences and self.work_preferences['keywords_whitelist']:
            query_builder.add_to_keywords(self.work_preferences['keywords_whitelist'])
        
        # Translate the unified query into a search-engine-specific query
        final_query, params = query_builder.build_query_for_engine(self.search_engine)
        
        # Store the final query for logging/debugging purposes
        self.current_query = final_query
        
        logger.info(f"Querying '{self.current_query}' with offset={self.search_offset} and limit={self.search_limit}")

        # Execute the search request using the chosen engine
        response = self.search_engine.search(
            query=final_query,
            params=params,
            offset=self.search_offset,
            limit=self.search_limit
        )

        logger.info(f"Found {len(response.results)} results for query '{self.current_query}'")

        # Store the results
        self.jobs = response.results


    def job_tile_to_job(self, job_tile: SearchResult) -> Job:
        raise NotImplementedError
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
        
