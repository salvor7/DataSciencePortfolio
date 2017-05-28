import requests
from os import path


project_gutenberg_bible_url = 'http://www.gutenberg.org/cache/epub/10/pg10.txt'
bible_filename = 'bible.txt'
bible_path = path.join('..', 'data', bible_filename)


def bible_text(url=project_gutenberg_bible_url):
    """Get the bible text"""
    return requests.get(url).text


def process_gutenberg_bible(url=project_gutenberg_bible_url):
    """Remove header and footer info"""
    text = bible_text(url)

    start_phrase = 'The First Book of Moses:  Called Genesis'
    end_phrase = 'End of the Project Gutenberg EBook of The King James Bible'
    assert text.count(start_phrase) == 1 and text.count(end_phrase) == 1

    start_idx, end_idx = text.find(start_phrase), text.find(end_phrase)

    return text[start_idx:end_idx]


def save_internet_bible(url=project_gutenberg_bible_url):
    """Save bible as a text file"""
    bible = process_gutenberg_bible(url)
    with open(bible_path, 'w') as file:
        file.write(bible)
