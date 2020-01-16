"""Main scrapper."""

# Config
from common import config

# Errors
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

# Utils
import argparse
import logging
import re
import csv
import news_page_object as news
from datetime import datetime

is_well_formed_link = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _news_scraper(new_site_uid):
    """Get site for scrape."""
    host = config()['new_sites'][new_site_uid]['url']
    articles = []
    logging.info('Beginning scrapper for {}'.format(host))
    homepage = news.HomePage(new_site_uid, host)

    for link in homepage.article_links:
        article = _fetch_article(new_site_uid, host, link)
        if article:
            logger.info('Article fetched.')
            articles.append(article)
    _save_articles(new_site_uid, articles)


def _save_articles(new_site_uid, articles):
    """Build file with articles."""
    now = datetime.now().strftime('%Y_%m_%d')
    file_name = '{}_{}_articles.csv'.format(new_site_uid, now)
    csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))
    with open(file_name, mode='w+') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)
        for article in articles:
            row = [str(getattr(article, prop)) for prop in csv_headers]
            writer.writerow(row)


def _fetch_article(new_site_uid, host, link):
    """Fetch articles function."""
    logger.info('Startin fetch article at: {}'.format(link))

    article = None
    try:
        article = news.ArticlePage(new_site_uid, _build_link(host, link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error fetchin article {}'.format(e), exc_info=False)
    
    if article and not article.body:
        logger.warning('Invalid article, there is not body.')
    
    return article


def _build_link(host, link):
    """Build link based on return from scraper."""
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host, link)
    else:
        return '{}/{}'.format(host, link)


if __name__ == "__main__":
    new_sites_choices = list(config()['new_sites'].keys())
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'new_site',
        help='The new site that you want to scrape.',
        type=str,
        choices=new_sites_choices
    )
    args = parser.parse_args()
    _news_scraper(args.new_site)
