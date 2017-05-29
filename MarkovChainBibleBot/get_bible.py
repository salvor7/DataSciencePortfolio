import requests
from os import path


project_gutenberg_bible_url = 'http://www.gutenberg.org/cache/epub/10/pg10.txt'
bible_filename = 'bible.txt'
bible_path = path.join('..', 'data', bible_filename)


def save_internet_bible(url=project_gutenberg_bible_url, path=bible_path):
    """Save bible as a text file"""
    bible = requests.get(url).text

    with open(path, 'w') as file:
        file.write(bible)


def process_gutenberg_bible(text):
    """Remove header and footer info"""
    start_phrase = 'The First Book of Moses:  Called Genesis'
    end_phrase = 'End of the Project Gutenberg EBook of The King James Bible'
    assert text.count(start_phrase) == 1 and text.count(end_phrase) == 1

    start_idx, end_idx = text.find(start_phrase), text.find(end_phrase)

    return text[start_idx:end_idx]


def read_gutenberg_bible():
    """Open and process the saved text of the bible"""
    with open(bible_path, 'r') as file:
        return process_gutenberg_bible(file.read())


if __name__ == '__main__':
    save_internet_bible()