from itertools import islice, chain
import six
from lxml import etree
from html import unescape as _unescape
import re
import bleach
from nltk.corpus import stopwords


# Efficient parsing of large XML files from
# http://stackoverflow.com/a/9814580/987185
def parse(fp):
    """Efficiently parses an XML file from the StackExchange data dump and
    returns a generator which yields one row at a time.
    """

    context = etree.iterparse(fp, events=("end",))

    for _, elem in context:
        if elem.tag == "row":
            # processing goes here
            assert elem.text is None, "The row wasn't empty"
            yield elem.attrib

        # cleanup
        # first empty children from current element
        # This is not absolutely necessary if you are also deleting
        # siblings, but it will allow you to free memory earlier.
        elem.clear()
        # second, delete previous siblings (records)
        while elem.getprevious() is not None:
            del elem.getparent()[0]
        # make sure you have no references to Element objects outside the loop


def batch(iterable, size):
    """Creates a batches of size `size` from the `iterable`."""
    sourceiter = iter(iterable)
    while True:
        batchiter = islice(sourceiter, size)
        try:
            yield chain([six.next(batchiter)], batchiter)
        except StopIteration:
            return


_WORD_RE = re.compile(r"\b\w+\b", flags=re.UNICODE)

def extract_id_and_body(attrs):
    """Return (id, body) from a row attributes dict, or (None, None) if no Body or Id is present.
    """
    pid = attrs.get('Id')
    body = attrs.get('Body')
    if pid is None or body is None:
        return None, None
    return pid, body


def clean_body_html(body):
    """Convert HTML entities and strip tags, returning plain text."""
    if body is None:
        return ''
    text = _unescape(body)
    cleaned = bleach.clean(text, tags=[], attributes={}, strip=True)
    return cleaned


def tokenize_text(text):
    """Lowercase and split text into word tokens using a simple regexp."""
    if not text:
        return []
    return [m.group(0).lower() for m in _WORD_RE.finditer(text)]


def remove_stopwords(tokens):
    """Remove common English stopwords from a list of tokens."""
    stop = set(stopwords.words('english'))
    return [t for t in tokens if t not in stop]


def shingles_from_tokens(tokens, k=5):
    """Return a set of k-word shingles."""
    if k <= 0:
        raise ValueError('k must be > 0')
    if len(tokens) < k:
        return set()
    return set(' '.join(tokens[i:i + k]) for i in range(len(tokens) - k + 1))


def process_post(attrs, k=5):
    """Given a row attributes dict, return (id, shingles_set)."""
    pid, body = extract_id_and_body(attrs)
    if pid is None:
        return None, set()
    cleaned = clean_body_html(body)
    tokens = tokenize_text(cleaned)
    tokens = remove_stopwords(tokens)
    shingles = shingles_from_tokens(tokens, k=k)
    return pid, shingles