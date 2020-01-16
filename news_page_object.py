"""News page objects."""

# Utils
import bs4
import requests
from common import config


class NewsPage:
    """Main class for news page."""

    def __init__(self, new_site_uid, url):
        """Initialize config for home page."""
        self._config = config()['new_sites'][new_site_uid]
        self._queries = self._config['queries']
        self._html = None
        self._visit_url(url)

    def _select(self, query_string):
        return self._html.select(query_string)

    def _visit_url(self, url):
        """Visit url for get content."""
        response = requests.get(url)
        response.raise_for_status()
        self._html = bs4.BeautifulSoup(response.text, 'html.parser')


class HomePage(NewsPage):
    """Home page class."""

    def __init__(self, new_site_uid, url):
        """Initialize config from news page."""
        super().__init__(new_site_uid, url)

    @property
    def article_links(self):
        """Get articles link of website."""
        links = []
        for link in self._select(self._queries['home_page_article_links']):
            if link and link.has_attr('href'):
                links.append(link)

        return set(link['href'] for link in links)


class ArticlePage(NewsPage):
    """Article page class."""

    def __init__(self, new_site_uid, url):
        """Initialize config from news page."""
        super().__init__(new_site_uid, url)

    @property
    def body(self):
        """Get article body."""
        result = self._select(self._queries['article_body'])
        return result[0].text if result else ''

    @property
    def title(self):
        """Get article title."""
        result = self._select(self._queries['article_title'])
        return result[0].text if result else ''