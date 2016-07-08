# -*- coding: utf-8 -*-
import scrapy
from urlparse import urljoin
from scrapy.http.request import Request

from socool.items import MFWItem


class MafengwoSpider(scrapy.Spider):
    name = "mafengwo"

    start_urls = ['http://www.www.mafengwo.cn/']

    def parse(self, response):

        url = 'http://www.mafengwo.cn/u/{0}.html'
        for uid in xrange(70000000, 99999999):
            yield Request(url.format(uid), callback=self.parse_user)

    def parse_user(self, reponse)
        item = MFWItem()

        item['name'] = response.xpath(
            '//div[@class="MAvaName"]/text()').extract_frist()
        item['level'] = response.xpath(
            '//span[@class="MAvaLevel flt1"]/a/@title').extract_frist()
        item['tags'] = reponse.xpath(
            '//div[@class="its_tags"]/a/@title').extract()
        item['attention'] = response.xpath(
            '//div[@class="MAvaMore clearfix"]//a/text()').extract()
        item['groups'] = reponse.xpath(
            '//div[@class="MGroupDetail"]//a[@class="name"]/text()').extract()
        item['dynamic'] = reponse.xpath(
            '//span[@class="time"]/text()').extract()
        item['note'] = {}
        item['path'] = {}
        item['together'] = {}
        note = reponse.xpath('//a[@title="TA的游记"]/@href').extract_frist()
        req = Request(urljoin(reponse.url, note), callback=self.parse_note)
        req.meta['item'] = item
        yield req

    def parse_note(self, reponse):
        item = response.meta['item']

        item['note']['count'] = response.xpath(
            '//div[@class="MAvaMore clearfix"]//a/text()').extract()
        item['note']['artices'] = []
        for note in response.xpath('//div[@class="notes_list"]//li'):
            item['note']['artices'].append(
                {
                    'title': note.xpath(''),

                }
            )

    notes = scrapy.Field()
    path = scrapy.Field()
    review = scrapy.Field()
    together = scrapy.Field()
