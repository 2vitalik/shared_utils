import re


def iterate_links_list(text):
    for line in text.split('\n'):
        m = re.fullmatch(r'# \[\[([^]]+)\]\]', line)
        if m:
            yield m.group(1)
