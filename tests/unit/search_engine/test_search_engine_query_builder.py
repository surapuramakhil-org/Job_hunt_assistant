from services.web_search_engine import SearchQueryBuilder, UnifiedQuery


def test_build_final_query_string_keywords_only():
    query = UnifiedQuery(keywords=["keyword1", "keyword2", "keyword3"])
    result = SearchQueryBuilder.build_final_query_string(query)
    assert result == "keyword1 keyword2 keyword3"

def test_build_final_query_string_with_whitelist():
    query = UnifiedQuery(
        keywords=["keyword1", "keyword2"],
        whitelist=["whitelist1", "whitelist2"]
    )
    result = SearchQueryBuilder.build_final_query_string(query)
    assert result == "keyword1 keyword2 (whitelist1 OR whitelist2)"

def test_build_final_query_string_with_blacklist():
    query = UnifiedQuery(
        keywords=["keyword1", "keyword2"],
        blacklist=["blacklist1", "blacklist2"]
    )
    result = SearchQueryBuilder.build_final_query_string(query)
    assert result == "keyword1 keyword2 (-blacklist1 OR -blacklist2)"

def test_build_final_query_string_with_multi_word_whitelist_and_blacklist():
    query = UnifiedQuery(
        keywords=["keyword1", "keyword2"],
        whitelist=["multi word whitelist1", "multi word whitelist2"],
        blacklist=["multi word blacklist1", "multi word blacklist2"]
    )
    result = SearchQueryBuilder.build_final_query_string(query)
    assert result == 'keyword1 keyword2 ("multi word whitelist1" OR "multi word whitelist2") (-"multi word blacklist1" OR -"multi word blacklist2")'

def test_build_final_query_string_with_whitelist_and_blacklist():
    query = UnifiedQuery(
        keywords=["keyword1", "keyword2"],
        whitelist=["whitelist1", "whitelist2"],
        blacklist=["blacklist1", "blacklist2"]
    )
    result = SearchQueryBuilder.build_final_query_string(query)
    assert result == "keyword1 keyword2 (whitelist1 OR whitelist2) (-blacklist1 OR -blacklist2)"

def test_build_final_query_string_empty_query():
    query = UnifiedQuery()
    result = SearchQueryBuilder.build_final_query_string(query)
    assert result == ""