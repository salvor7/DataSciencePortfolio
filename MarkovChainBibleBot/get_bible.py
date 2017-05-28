import requests
from os import path, linesep


project_gutenberg_bible_url = 'http://www.gutenberg.org/cache/epub/10/pg10.txt'
bible_filename = 'bible.txt'
bible_path = path.join('..', 'data', bible_filename)


def bible_text(url=project_gutenberg_bible_url):
    """Get the bible text"""
    return requests.get(url).text


def process_gutenberg_bible(url=project_gutenberg_bible_url):
    """Remove header and footer info"""
    gutenberg_header_footer_sep = linesep*8
    header, body, footer = bible_text(url).split(gutenberg_header_footer_sep)
    return body


def save_internet_bible(url=project_gutenberg_bible_url):
    """Save bible as a text file"""
    bible = process_gutenberg_bible(url)
    with open(bible_path, 'w') as file:
        file.write(bible)
