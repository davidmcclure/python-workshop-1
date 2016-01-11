

import requests
import re
import click

from collections import OrderedDict
from stop_words import get_stop_words


def download_text(url):

    """
    Load a URL and return the raw page content.

    Args:
        url (str)

    Returns: str
    """

    return requests.get(url).text


def extract_word_types(text):

    """
    Given a raw text, construct an ordered dictionary of {token -> count},
    sorted in descending order.

    Args:
        text (str)

    Returns:
        OrderedDict: Sorted word types.
    """

    counts = OrderedDict()

    # Match sequences of letters.
    tokens = re.finditer('[a-z]{2,}', text.lower())

    # Get English stopwords
    stopwords = get_stop_words('en')

    for match in tokens:

        token = match.group(0)

        # Skip stopwords.
        if token in stopwords:
            continue

        # If we've already seen the word, increment the count.
        if token in counts:
            counts[token] += 1

        # Otherwise, initialize the count to 1.
        else:
            counts[token] = 1

    return sort_dict(counts)


def sort_dict(d, desc=True):

    """
    Sort an ordered dictionary by value, descending.

    Args:
        d (OrderedDict): An ordered dictionary.
        desc (bool): If true, sort desc.

    Returns:
        OrderedDict: The sorted dictionary.
    """

    sort = sorted(d.items(), key=lambda x: x[1], reverse=desc)
    return OrderedDict(sort)


@click.command()
@click.argument('url')
@click.option('--n', default=50, help='Show the top N words.')
def count_words(url, n):

    """
    Count words in a text.
    """

    text = download_text(url)

    counts = extract_word_types(text)

    for word, count in list(counts.items())[:n]:
        print(word, count)


if __name__ == '__main__':
    count_words()
