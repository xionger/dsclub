import re
import time
import os
from datetime import datetime, timedelta
from pytz import UTC

import requests
import unidecode
from flask import session, url_for, flash, redirect, request, g
from jinja2 import Markup

from werkzeug.local import LocalProxy

from app._compat import range_method, text_type, iteritems, to_unicode, to_bytes

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug.
    Taken from the Flask Snippets page.
    :param text: The text which should be slugified
    :param delim: Default "-". The delimeter for whitespace
    """
    text = unidecode.unidecode(text)
    result = []
    for word in _punct_re.split(text.lower()):
        if word:
            result.append(word)
    return text_type(delim.join(result))
