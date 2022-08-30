#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Dror Atariah"
SITENAME = "Dr. Dror"
SITESUBTITLE = 'Foo is not just a "Bar"'
SITEURL = "https://drorata.github.io"

PATH = "content"

TIMEZONE = "Europe/Paris"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (
#     ("LinkedIn", "https://www.linkedin.com/in/atariah"),
#     ("GitHub", "http://github.com/drorata/"),
# )
ICONS = (
    ("github", "https://github.com/drorata"),
    ("linkedin", "https://www.linkedin.com/in/atariah"),
    # ("fas fa-envelope", "mailto:drorata@gmail.com"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = 10
DEFAULT_CATEGORY = "General"
DEFAULT_METADATA = {
    "status": "draft",
}
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
ARTICLE_URL = "posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/"
ARTICLE_SAVE_AS = "posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/index.html"

STATIC_PATHS = ["images", "files", "extra/favicon.ico", "extra/keybase.txt"]
EXTRA_PATH_METADATA = {
    "extra/favicon.ico": {"path": "favicon.ico"},
    "extra/keybase.txt": {"path": "keybase.txt"},
}

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.toc": {},
        "markdown.extensions.meta": {},
    },
    "output_format": "html5",
}

THEME = "themes/pelican-alchemy/alchemy"
SITEIMAGE = "/images/colored-spiral-of-roots.png width=90 height=90"

DISQUS_SITENAME = "dr-dror"
GOOGLE_ANALYTICS = "G-WH47T9F1TR"

# SEARCH_BOX = True
HIDE_AUTHORS = True
