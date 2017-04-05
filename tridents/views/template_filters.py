from flask import Markup
from tridents import app

from bleach import clean
from bs4 import BeautifulSoup
from arrow import Arrow
from markdown import markdown


@app.template_filter('datetimeformat')
def datetimeformat(value: Arrow, format='%H:%M %m/%d/%Y'):
    return value.to('US/Eastern').strftime(format)


@app.template_filter('markdown')
def markdown_to_html(content):
    # Markup marks text as safe for jinja (so tags won't get escaped)
    # sanitize with bleach as a precaution (even though post form isn't public)
    return Markup(markdown(clean(content)))


@app.template_filter('truncate_html')
def truncate_html(html, length=160):
    truncated = str(BeautifulSoup(html[:length], "html.parser"))
    if len(truncated) < len(html):
        truncated += "<span>...</span>"

    return Markup(truncated)
