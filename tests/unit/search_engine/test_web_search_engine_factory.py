from unittest.mock import patch

import pytest
from services.web_search_engine import GoogleSearchEngine, WebSearchEngineFactory


#TODO: patch is not working, its not mocking the ALLOWED_SEARCH_ENGINES in the config.py for tests, for now set it to same value of config.py
def test_web_search_engine_factory():
    with patch("config.ALLOWED_SEARCH_ENGINES", ["google", "bing", "brave"]), \
         patch("config.GOOGLE_SEARCH_ENGINE_ID", "mock_id"), \
         patch("config.GOOGLE_API_KEY", "mock_api_key"), \
         patch("config.BING_API_KEY", "mock_bing_api_key"), \
         patch("config.BRAVE_API_KEY", "mock_brave_api_key"):

        google_engine = WebSearchEngineFactory.get_search_engine("google")
        assert isinstance(google_engine, GoogleSearchEngine)

def test_web_search_engine_factory_singleton():
    with patch("config.ALLOWED_SEARCH_ENGINES", ["google"]), \
         patch("config.GOOGLE_SEARCH_ENGINE_ID", "mock_id"), \
         patch("config.GOOGLE_API_KEY", "mock_api_key"), \
         patch("config.BING_API_KEY", "mock_bing_api_key"), \
         patch("config.BRAVE_API_KEY", "mock_brave_api_key"):
    
        brave_engine_1 = WebSearchEngineFactory.get_search_engine("google")
        brave_engine_2 = WebSearchEngineFactory.get_search_engine("google")
        assert brave_engine_1 is brave_engine_2

def test_web_search_engine_factory_allowed_engines():
    with patch("config.ALLOWED_SEARCH_ENGINES", ["google"]), \
         patch("config.GOOGLE_SEARCH_ENGINE_ID", "mock_id"), \
         patch("config.GOOGLE_API_KEY", "mock_api_key"), \
         patch("config.BING_API_KEY", "mock_bing_api_key"), \
         patch("config.BRAVE_API_KEY", "mock_brave_api_key"):
    
        for engine_name in ["google"]:
            engine = WebSearchEngineFactory.get_search_engine(engine_name)
            assert engine is not None



