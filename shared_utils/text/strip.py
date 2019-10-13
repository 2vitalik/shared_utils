import re


def strip(text):
    if not text:  # для случая None
        return ''
    return text.strip()


def remove_spaces(text):
    """To be used in multiline strings."""
    return re.sub('\n +', '\n', text)
