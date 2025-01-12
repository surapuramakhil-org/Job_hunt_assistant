import pytest
from src.services.web_search_engine import GoogleSearchEngine, BingSearchEngine, BraveSearchEngine

@pytest.mark.integration
def test_google_search_engine_integration():
    search_engine = GoogleSearchEngine()  # Replace with a valid ID
    pagenated_response = search_engine.search("Python integration testing")

    assert len(pagenated_response.results) > 0

# @pytest.mark.integration
# def test_bing_search_engine_integration():
#     search_engine = BingSearchEngine()
#     result = search_engine.search("Python integration testing")

#     assert "webPages" in result
#     assert "value" in result["webPages"]
#     assert len(result["webPages"]["value"]) > 0

# @pytest.mark.integration
# def test_brave_search_engine_integration():
#     search_engine = BraveSearchEngine()
#     result = search_engine.search("Python integration testing")

#     assert "results" in result
#     assert len(result["results"]) > 0
