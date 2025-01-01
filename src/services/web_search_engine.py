from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import requests
from abc import ABC, abstractmethod
import src.config as config
from src.config import ALLOWED_SEARCH_ENGINES, GOOGLE, BING, BRAVE
from src.logger import logger

@dataclass
class SearchResult:
    """
    Represents an individual search result item.
    Note: 'engine_name' is moved to PaginatedSearchResponse.
    """
    title: str
    link: str
    snippet: str
    raw_data: Optional[Dict[str, Any]] = field(default=None)


@dataclass
class PaginatedSearchResponse:
    """
    Holds a list of SearchResult items plus offset-based pagination info
    and the 'engine_name' to identify which engine provided these results.
    """
    results: List[SearchResult] = field(default_factory=list)
    engine_name: str = ""
    offset: int = 0
    limit: int = 10
    total_results: Optional[int] = None


class WebSearchEngine(ABC):
    """
    Abstract base class for web search engines. Each subclass's search
    method returns a PaginatedSearchResponse object.
    """
    @abstractmethod
    def search(self, query: str, offset: int = 0, limit: int = 10) -> PaginatedSearchResponse:
        """
        Perform an offset-based search with the specified limit (number
        of results per request).
        """
        pass


class GoogleSearchEngine(WebSearchEngine):
    GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(self):
        self.api_key = config.GOOGLE_API_KEY
        self.search_engine_id = config.GOOGLE_SEARCH_ENGINE_ID

    def search(self, query: str, offset: int = 0, limit: int = 10) -> PaginatedSearchResponse:
        """
        Google uses 'start' to represent offset. 
        If offset is 0, start=1. If offset is 10, start=11, etc.
        """
        start = offset + 1
        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "start": start,
            "num": limit
        }
        response = requests.get(self.GOOGLE_SEARCH_URL, params=params)
        response.raise_for_status()
        return self._parse_response(response.json(), offset, limit)

    def _parse_response(
        self,
        response: Dict[str, Any],
        offset: int,
        limit: int
    ) -> PaginatedSearchResponse:
        results: List[SearchResult] = []
        for item in response.get("items", []):
            results.append(SearchResult(
                title=item.get("title", ""),
                link=item.get("link", ""),
                snippet=item.get("snippet", ""),
                raw_data=item
            ))

        # Extract totalResults from "searchInformation"
        search_info = response.get("searchInformation", {})
        total_str = search_info.get("totalResults")
        total_results = int(total_str) if total_str and total_str.isdigit() else None

        return PaginatedSearchResponse(
            results=results,
            engine_name="Google",
            offset=offset,
            limit=limit,
            total_results=total_results
        )


class BingSearchEngine(WebSearchEngine):
    BING_SEARCH_URL = "https://api.bing.microsoft.com/v7.0/search"

    def __init__(self):
        self.api_key = config.BING_API_KEY

    def search(self, query: str, offset: int = 0, limit: int = 50) -> PaginatedSearchResponse:
        """
        Bing uses 'offset' in addition to 'count' (our limit).
        """
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        params = {
            "q": query,
            "offset": offset,
            "count": limit
        }
        response = requests.get(self.BING_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        return self._parse_response(response.json(), offset, limit)

    def _parse_response(
        self,
        response: Dict[str, Any],
        offset: int,
        limit: int
    ) -> PaginatedSearchResponse:
        results: List[SearchResult] = []
        web_pages = response.get("webPages", {})
        for item in web_pages.get("value", []):
            results.append(SearchResult(
                title=item.get("name", ""),
                link=item.get("url", ""),
                snippet=item.get("snippet", ""),
                raw_data=item
            ))

        total_estimated = web_pages.get("totalEstimatedMatches")
        total_results = total_estimated if isinstance(total_estimated, int) else None

        return PaginatedSearchResponse(
            results=results,
            engine_name="Bing",
            offset=offset,
            limit=limit,
            total_results=total_results
        )


class BraveSearchEngine(WebSearchEngine):
    BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"

    def __init__(self):
        self.api_key = config.BRAVE_API_KEY

    def search(self, query: str, offset: int = 0, limit: int = 20) -> PaginatedSearchResponse:
        """
        Brave also supports 'offset' (number of items to skip) and 'limit'.
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {
            "q": query,
            "offset": offset,
            "limit": limit
        }
        response = requests.get(self.BRAVE_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        return self._parse_response(response.json(), offset, limit)

    def _parse_response(
        self,
        response: Dict[str, Any],
        offset: int,
        limit: int
    ) -> PaginatedSearchResponse:
        results: List[SearchResult] = []
        web_data = response.get("web", {})
        for item in web_data.get("results", []):
            results.append(SearchResult(
                title=item.get("title", ""),
                link=item.get("url", ""),
                snippet=item.get("description", ""),
                raw_data=item
            ))
        # Brave often doesn’t provide total results
        total_results = None

        return PaginatedSearchResponse(
            results=results,
            engine_name="Brave",
            offset=offset,
            limit=limit,
            total_results=total_results
        )


class WebSearchEngineFactory:
    _instances = {}

    @staticmethod
    def get_search_engine(engine_name=None):
        if engine_name is None:
            # For now, just pick the first allowed search engine
            engine_name = ALLOWED_SEARCH_ENGINES[0]

        engine_name = engine_name.lower()
        
        if engine_name not in ALLOWED_SEARCH_ENGINES:
            raise ValueError(f"Search engine {engine_name} is not allowed. Allowed engines: {ALLOWED_SEARCH_ENGINES}")

        if engine_name in WebSearchEngineFactory._instances:
            return WebSearchEngineFactory._instances[engine_name]

        if engine_name == GOOGLE:
            search_engine_id = config.GOOGLE_SEARCH_ENGINE_ID
            instance = GoogleSearchEngine()
        elif engine_name == BING:
            instance = BingSearchEngine()
        elif engine_name == BRAVE:
            instance = BraveSearchEngine()
        else:
            raise ValueError(f"Unknown search engine: {engine_name}")

        WebSearchEngineFactory._instances[engine_name] = instance
        return instance
    

