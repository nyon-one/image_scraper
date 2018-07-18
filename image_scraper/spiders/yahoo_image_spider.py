# -*- coding: utf-8 -*-

import scrapy
from image_scraper.items import ImageScraperItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor



DOWNLOAD_LIMIT = 1000


class YahooImageSpider(CrawlSpider):

    name = 'yahoo_image'

    rules = (
        Rule(LinkExtractor(allow=( )), callback="parse", follow=True),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_id = 0

    def start_requests(self):
        url = ('https://search.yahoo.co.jp/image/search?'
               'p={}&ei=UTF-8&save=0'.format(self.query))
        yield scrapy.Request(url, self.parse, dont_filter=True)

    def parse(self, response):
        items = ImageScraperItem()
        items['member_id'] = self.member_id
        items['image_ids'] = []
        items['image_urls'] = []

        for src in response.css('#gridlist > div'):
            self.image_id += 1

            url = src.css('div > p > a::attr(href)').extract_first()
            items['image_ids'].append(self.image_id)
            items['image_urls'].append(url)

        yield items

        css_next_page = '#Sp1 > p > span.m > a::attr(href)'
        next_page = response.css(css_next_page).extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
