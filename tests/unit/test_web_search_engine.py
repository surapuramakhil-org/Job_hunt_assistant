import pytest
from unittest.mock import patch, MagicMock
from src.services.web_search_engine import GoogleSearchEngine, BingSearchEngine, BraveSearchEngine

# Unit test for GoogleSearchEngine
@patch("requests.get")
@patch("src.config.GOOGLE_API_KEY", "mock_api_key")  # Mocking the Google API key
@patch("src.config.GOOGLE_SEARCH_ENGINE_ID", "mock_id")  # Mocking the Google Search Engine ID
def test_google_search_engine(mock_get):
    mock_response = MagicMock()
    # Mocking a valid Google API response
    mock_response.json.return_value = {
        "items": [
            {"title": "result1", "link": "http://example.com/1", "snippet": "Snippet 1"},
            {"title": "result2", "link": "http://example.com/2", "snippet": "Snippet 2"}
        ],
        "searchInformation": {"totalResults": "2"}
    }
    mock_get.return_value = mock_response

    search_engine = GoogleSearchEngine()
    result = search_engine.search("test query")

    mock_get.assert_called_once_with(
        "https://www.googleapis.com/customsearch/v1",
        params={"key": "mock_api_key", "cx": "mock_id", "q": "test query", "start": 1, "num": 10},
    )
    assert len(result.results) == 2
    assert result.results[0].title == "result1"
    assert result.results[0].link == "http://example.com/1"
    assert result.results[0].snippet == "Snippet 1"

# Unit test for BingSearchEngine
@patch("requests.get")
@patch("src.config.BING_API_KEY", "mock_bing_api_key")  # Mocking the Bing API key
def test_bing_search_engine(mock_get):
    mock_response = MagicMock()
    # Mocking a valid Bing API response
    mock_response.json.return_value = {
        "webPages": {
            "value": [
                {"name": "result1", "url": "http://example.com/1", "snippet": "Snippet 1"},
                {"name": "result2", "url": "http://example.com/2", "snippet": "Snippet 2"}
            ],
            "totalEstimatedMatches": 2
        }
    }
    mock_get.return_value = mock_response

    search_engine = BingSearchEngine()
    result = search_engine.search("test query", limit=10)

    mock_get.assert_called_once_with(
        "https://api.bing.microsoft.com/v7.0/search",
        headers={"Ocp-Apim-Subscription-Key": "mock_bing_api_key"},
        params={"q": "test query", "count": 10, "offset": 0},
    )
    assert len(result.results) == 2
    assert result.results[0].title == "result1"
    assert result.results[0].link == "http://example.com/1"
    assert result.results[0].snippet == "Snippet 1"

# Unit test for BraveSearchEngine
@patch("requests.get")
@patch("src.config.BRAVE_API_KEY", "mock_brave_api_key")  # Mocking the Brave API key
def test_brave_search_engine(mock_get):
    mock_response = MagicMock()
    # Mocking a valid Brave API response
    mock_response.json.return_value = {
        "web": {
            "results": [
                {"title": "result1", "url": "http://example.com/1", "description": "Snippet 1"},
                {"title": "result2", "url": "http://example.com/2", "description": "Snippet 2"}
            ]
        }
    }
    mock_get.return_value = mock_response

    search_engine = BraveSearchEngine()
    result = search_engine.search("test query", limit=10)

    mock_get.assert_called_once_with(
        "https://api.search.brave.com/res/v1/web/search",
        headers={"Authorization": f"Bearer mock_brave_api_key"},
        params={"q": "test query", "offset": 0, "limit": 10},
    )
    assert len(result.results) == 2
    assert result.results[0].title == "result1"
    assert result.results[0].link == "http://example.com/1"
    assert result.results[0].snippet == "Snippet 1"
