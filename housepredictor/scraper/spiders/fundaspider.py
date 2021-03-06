import json
import sys

import scrapy
from scrapy import Request
import codecs
import timeit

#from housepredictor.scraper.items import FundaItem


def get_search_url(api_key='16F03929-0DB2-4FA7-8B55-182D9B20404A',
                   type='koop', zone='heel-nederland',
                   page=1, page_size=25):
    """Returns a funda search url for the given arguments

    :param api_key: the api key to use for funda. the default one is for the
    mobile app
    :param type: the type of the listings. Currently can be `koop` or
    `huur`
    :param zone: the zone to search. default
    :param page: the result page
    :param page_size: the size of the pages, currently the maximum is 25"""
    url_template = 'http://partnerapi.funda.nl/feeds/Aanbod.svc/json/{' \
                   'api_key}/?type={type}&zo={query}&page={' \
                   'page}&page_size={page_size}&website=funda'
    query = '/{zone}/'.format(zone=zone)
    format_args = {
        'api_key': api_key,
        'page': page,
        'page_size': page_size,
        'query': query,
        'type': type
    }
    return url_template.format(**format_args)


def get_detail_url(listing_id, api_key='16F03929-0DB2-4FA7-8B55-182D9B20404A',
                   type='koop'):
    """Returns the page detail for the given listing_id"""

    url_template = 'http://partnerapi.funda.nl/feeds/Aanbod.svc/detail' \
                   '/{api_key}/{type}/globalid/{listing_id}/'
    format_args = {
        'api_key': api_key,
        'type': type,
        'listing_id': listing_id
    }
    return url_template.format(**format_args)


class FundaSpider(scrapy.Spider):
    name = 'fundaspider'

    def __init__(self, *args, **kwargs):
        """Initializes the spider.
        Receives additional arguments to specify to the search url.
        Currently supported arguments:
            * type: `koop` or `huur`
            * zone: the zone where to search for properties
            * api_key: the api key to use. currently the mobile app api-key
            * all: whether to scrape all data or return just the relevant fields(not recommended)
        """
        self.search_args = {
            'type': kwargs.pop('type', 'koop'),
            'zone': kwargs.pop('zone', 'heel-nederland'),
            'api_key': kwargs.pop('api_key',
                                  '16F03929-0DB2-4FA7-8B55-182D9B20404A')
        }
        self.search_args.update(kwargs.pop('search_args', {}))
        self.sanitize = kwargs.pop('sanitize', True)  # whether to scrape all, or just data fields from json
        super().__init__(*args, **kwargs)

    def start_requests(self):
        # initiate the request to the first page
        yield self.build_page_request(1)

    def parse_detail(self, response):
        """Parses a page view of property and returns it's content and
        the list data received through the meta"""

        start_time = timeit.default_timer()

        posting = response.meta['list_posting']
        json_response = json.loads(response.body_as_unicode())  # parse json
        posting.update(json_response)
        


        # data is fairly consistent across the api so no
        # scrpy items are fairly redundant
        return posting

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        # deal with the paging
        total_pages = json_response['Paging']['AantalPaginas']
        current_page = json_response['Paging']['HuidigePagina']

        # iterate over all postings on the page
        for posting in json_response['Objects']:
            req = self.build_detail_request(posting['GlobalId']) #
            req.meta['list_posting'] = posting
            yield req

        if current_page < total_pages:
            # there still are pages left
            yield self.build_page_request(current_page)

    def build_page_request(self, page):
        """Returns the request for a given page and the spider's search
        arguments"""
        page_url = get_search_url(page=page + 1, **self.search_args)
        return Request(page_url)

    def build_detail_request(self, global_id):
        """Returns a request for the detail page of a property
        :param global_id: the i of the posting"""
        detail_url = get_detail_url(listing_id=global_id,
                                    type=self.search_args['type'],
                                    api_key=self.search_args['api_key'])

        return Request(detail_url,
                       callback=self.parse_detail)
