import re

def clean_text(text: str) -> str:
    """
    Cleans raw text by normalizing whitespace.
    """
    if not text:
        return ""
    # Replace multiple spaces/newlines with a single one
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_email(text: str) -> str:
    """
    Extracts the first email address found in the text.
    """
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group(0) if match else "Not found"

def extract_phone(text: str) -> str:
    """
    Extracts the first phone number found in the text.
    Supports formats like +1-234-567-8901, 1234567890, etc.
    """
    pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    match = re.search(pattern, text)
    return match.group(0) if match else "Not found"

def estimate_word_count(text: str) -> int:
    """
    Estimates word count.
    """
    if not text:
        return 0
    return len(text.split())
