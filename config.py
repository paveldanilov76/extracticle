import logging
import sys

logging.basicConfig(format=u'%(message)s', level=logging.DEBUG, stream=sys.stdout)

WORDS_PATTERN = r'\b\w+\b'
SENTENCE_PATTERN = r'\s*[^.!?]*[.!?]'

TRAIT_PATTERN = SENTENCE_PATTERN
MAX_WIDTH = 80
CONTAINER_TAGS = ['article', 'div', 'html', 'iframe', 'section']
CONTENT_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'p']
# CONTENT_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'p', 'address', 'q', 'blockquote', 'pre', 'ul']
