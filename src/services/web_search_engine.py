from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Tuple
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


class SearchTimeRange(Enum):
    LAST_24_HOURS = "last_24_hours"
    LAST_WEEK = "last_week"
    LAST_MONTH = "last_month"
    # TODO: add custom range later


@dataclass
class CustomTimeRange:
    start_time: datetime
    end_time: datetime


@dataclass
class UnifiedQuery:
    """
    Represents a unified search query that can be translated into
    platform-specific queries.
    """
    keywords: List[str] = field(default_factory=list)
    blacklist: List[str] = field(default_factory=list)
    whitelist: List[str] = field(default_factory=list)
    date_range: Optional[SearchTimeRange] = None
    gl: Optional[str] = None


class WebSearchEngine(ABC):

    @property
    @abstractmethod
    def DEFAULT_SEARCH_LIMIT(self) -> int:
        """
        Returns the default search limit for the search engine.
        """
        pass

    """
    Abstract base class for web search engines.
    Each subclass's search method returns a PaginatedSearchResponse object.
    """
    @abstractmethod
    def search(self, query: str, params: dict, offset: int = 0, limit: int = 10) -> PaginatedSearchResponse:
        """
        Perform an offset-based search with the specified limit (number 
        of results per request).
        """
        pass

    @abstractmethod
    def build_query(self, query: UnifiedQuery) -> Tuple[str, dict]:
        """
        Returns a tuple containing:
          - A query string
          - A parameters dictionary
        specific to the search engine.
        """
        pass


class SearchQueryBuilder:
    """
    A builder class for creating unified search queries.

    blacklist => (-blacklistitem1 OR -blacklistitem2 OR ...)
    whitelist => (whitelistitem1 OR whitelistitem2 OR ...)
    keywords  => keyworditem1 keyworditem2 keyworditem3

    final query will be = keywords + (whitelist) + (blacklist)
    Example:
      keyworditem1 keyworditem2 keyworditem3
      (whitelistitem1 OR whitelistitem2 OR ...)
      (-blacklistitem1 OR -blacklistitem2 OR ...)

    Use double quotes "" for exact match if needed.
    """

    def __init__(self):
        self.keywords: List[str] = []
        self.blacklist: List[str] = []
        self.whitelist: List[str] = []
        self.date_range: Optional[SearchTimeRange] = None
        self.gl: Optional[str] = None

    @staticmethod
    def create() -> "SearchQueryBuilder":
        return SearchQueryBuilder()

    def add_to_blacklist(self, term: Union[str, List[str]]) -> "SearchQueryBuilder":
        if isinstance(term, list):
            self.blacklist.extend(term)
        else:
            self.blacklist.append(term)
        return self

    def add_to_whitelist(self, term: Union[str, List[str]]) -> "SearchQueryBuilder":
        if isinstance(term, list):
            self.whitelist.extend(term)
        else:
            self.whitelist.append(term)
        return self

    def add_to_keywords(self, term: Union[str, List[str]]) -> "SearchQueryBuilder":
        if isinstance(term, list):
            self.keywords.extend(term)
        else:
            self.keywords.append(term)
        return self

    def set_date_range(self, date_range: SearchTimeRange) -> "SearchQueryBuilder":
        if not isinstance(date_range, SearchTimeRange):
            raise ValueError("date_range must be an instance of SearchTimeRange Enum")
        self.date_range = date_range
        return self

    def set_geolocation(self, gl: str) -> "SearchQueryBuilder":
        self.gl = gl
        return self

    def build_unified_query(self) -> UnifiedQuery:
        """
        Builds and returns a UnifiedQuery object.
        """
        return UnifiedQuery(
            keywords=self.keywords,
            blacklist=self.blacklist,
            whitelist=self.whitelist,
            date_range=self.date_range,
            gl=self.gl
        )
    
    def build_query_for_engine(self, serach_engine : WebSearchEngine) -> Tuple[str, dict]:
        return serach_engine.build_query(self.build_unified_query())

    @staticmethod
    def build_final_query_string(unified_query : UnifiedQuery) -> str:
        """
        Constructs and returns the final query string as described in the docstring:
        keywords + (whitelist) + (blacklist).

        Example:
            keyword1 keyword2 (whitelist1 OR whitelist2) (-black1 OR -black2)
        """
        # 1. Join keywords
        keywords_part = " ".join(unified_query.keywords)

        # 2. Build whitelist portion as (whitelist1 OR whitelist2 OR ...)
        whitelist_part = ""
        if unified_query.whitelist:
            whitelist_part = "(" + " OR ".join(unified_query.whitelist) + ")"

        # 3. Build blacklist portion as (-blacklist1 OR -blacklist2 OR ...)
        blacklist_part = ""
        if unified_query.blacklist:
            negated = [f"-{b}" for b in unified_query.blacklist]
            blacklist_part = "(" + " OR ".join(negated) + ")"

        # Combine them, skipping empty parts
        parts = [keywords_part, whitelist_part, blacklist_part]
        final_query = " ".join(p for p in parts if p)
        return final_query


class GoogleSearchEngine(WebSearchEngine):
    GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"
    @property
    def DEFAULT_SEARCH_LIMIT(self) -> int:
        return 10

    def __init__(self):
        self.api_key = config.GOOGLE_API_KEY
        self.search_engine_id = config.GOOGLE_SEARCH_ENGINE_ID

    def search(self, query: str, params: dict = {}, offset: int = 0, limit: int = DEFAULT_SEARCH_LIMIT) -> PaginatedSearchResponse:
        """
        Google uses 'start' to represent offset. 
        If offset is 0, start=1. If offset is 10, start=11, etc.
        """
        start = offset + 1
        params.update({
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "start": start,
            "num": limit
        })

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
        try:
            total_results = int(total_str)
        except (TypeError, ValueError):
            total_results = None

        return PaginatedSearchResponse(
            results=results,
            engine_name="Google",
            offset=offset,
            limit=limit,
            total_results=total_results
        )

    def build_query(self, query: UnifiedQuery) -> Tuple[str, dict]:
        """
        Builds a Google-specific query string and parameters, optionally adding
        date range and geolocation (gl).
        
        Returns:
          (query_string, params_dict)
        """
        # Use the static method from SearchQueryBuilder to build the final query string
        base_query = SearchQueryBuilder.build_final_query_string(query)
        params: Dict[str, Any] = {}

        # Handle geolocation as a separate parameter
        if query.gl:
            params["gl"] = query.gl

        # Handle date range (Google doesn't have direct date range in custom search)
        if query.date_range == SearchTimeRange.LAST_24_HOURS:
            params["dateRestrict"] = "d1"
        elif query.date_range == SearchTimeRange.LAST_WEEK:
            params["dateRestrict"] = "d7"
        elif query.date_range == SearchTimeRange.LAST_MONTH:
            params["dateRestrict"] = "d30"

        return base_query, params


class BingSearchEngine(WebSearchEngine):
    BING_SEARCH_URL = "https://api.bing.microsoft.com/v7.0/search"
    @property
    def DEFAULT_SEARCH_LIMIT(self) -> int:
        return 50

    def __init__(self):
        self.api_key = config.BING_API_KEY

    def search(self, query: str, params: dict = {}, offset: int = 0, limit: int = DEFAULT_SEARCH_LIMIT) -> PaginatedSearchResponse:
        """
        Bing uses 'offset' in addition to 'count' (our limit).
        """
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        params.update({
            "q": query,
            "offset": offset,
            "count": limit
        })

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

    def build_query(self, query: UnifiedQuery) -> Tuple[str, dict]:
        """
        Builds a Bing-specific query string and parameters, optionally adding
        date range and geolocation (mkt).
        
        Returns:
          (query_string, params_dict)
        """
        base_query = SearchQueryBuilder.build_final_query_string(query)

        params: Dict[str, Any] = {}

        # Geolocation (market code)
        if query.gl:
            params["mkt"] = query.gl

        # Date range via 'freshness' param
        if query.date_range == SearchTimeRange.LAST_24_HOURS:
            params["freshness"] = "Day"
        elif query.date_range == SearchTimeRange.LAST_WEEK:
            params["freshness"] = "Week"
        elif query.date_range == SearchTimeRange.LAST_MONTH:
            params["freshness"] = "Month"

        return base_query, params


class BraveSearchEngine(WebSearchEngine):
    BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"
    @property
    def DEFAULT_SEARCH_LIMIT(self) -> int:
        return 20

    def __init__(self):
        self.api_key = config.BRAVE_API_KEY

    def search(self, query: str, params: dict = {}, offset: int = 0, limit: int = DEFAULT_SEARCH_LIMIT) -> PaginatedSearchResponse:
        """
        Brave also supports 'offset' (number of items to skip) and 'limit'.
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params.update({
            "q": query,
            "offset": offset,
            "limit": limit
        })

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

    def build_query(self, query: UnifiedQuery) -> Tuple[str, dict]:
        """
        Builds a Brave-specific query string and parameters, optionally adding
        date range and geolocation (loc).
        
        Returns:
          (query_string, params_dict)
        """
        base_query = SearchQueryBuilder.build_final_query_string(query)
        params: Dict[str, Any] = {}

        # Geolocation
        if query.gl:
            params["loc"] = query.gl

        # Date range using custom pseudo-operators
        if query.date_range == SearchTimeRange.LAST_24_HOURS:
            base_query += " past:24h"
        elif query.date_range == SearchTimeRange.LAST_WEEK:
            base_query += " past:7d"
        elif query.date_range == SearchTimeRange.LAST_MONTH:
            base_query += " past:30d"

        return base_query, params


class WebSearchEngineFactory:
    _instances: Dict[str, WebSearchEngine] = {}

    @staticmethod
    def get_search_engine(engine_name: Optional[str] = None) -> WebSearchEngine:
        if engine_name is None:
            # For now, just pick the first allowed search engine
            engine_name = ALLOWED_SEARCH_ENGINES[0]

        engine_name = engine_name.lower()
        if engine_name not in ALLOWED_SEARCH_ENGINES:
            raise ValueError(
                f"Search engine '{engine_name}' is not allowed. "
                f"Allowed engines: {ALLOWED_SEARCH_ENGINES}"
            )

        if engine_name in WebSearchEngineFactory._instances:
            return WebSearchEngineFactory._instances[engine_name]

        if engine_name == GOOGLE:
            instance = GoogleSearchEngine()
        elif engine_name == BING:
            instance = BingSearchEngine()
        elif engine_name == BRAVE:
            instance = BraveSearchEngine()
        else:
            raise ValueError(f"Unknown search engine: {engine_name}")

        WebSearchEngineFactory._instances[engine_name] = instance
        return instance
