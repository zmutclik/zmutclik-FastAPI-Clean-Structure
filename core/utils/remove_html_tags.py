import re


def remove_html_tags(text: str) -> str:
    clean_text = re.sub(r"<.*?>", "", text)
    return clean_text
