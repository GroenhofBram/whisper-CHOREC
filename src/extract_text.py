from re import match, search

pattern = r'\((.*?)\)'

def extract_text(text) -> str:
    match = search(pattern, text)
    if match:
        return match.group(1)
    else:
        return text