def is_multi_word(string: str) -> bool:
    return ' ' in string or len(string.split()) > 1