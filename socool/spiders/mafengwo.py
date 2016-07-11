# -*- coding: utf-8 -*-
import scrapy
from urlparse import urljoin
from collections import defaultdict
from scrapy.http.request import Request

from socool.items import MFWItem


class MafengwoSpider(scrapy.Spider):
    name = "mafengwo"

    start_urls = ['http://www.mafengwo.cn/']

    def parse(self, response):

        url = 'http://www.mafengwo.cn/u/{0}.html'
        # for uid in xrange(100000, 20000000):
        # 600000
        for uid in xrange(10200000, 10400000):
            yield Request(url.format(uid), callback=self.parse_user, meta={'uid':uid})

    def parse_user(self, response):
        item = MFWItem()

        item['uid'] = response.meta['uid']
        item['name'] = response.xpath(
            '//div[@class="MAvaName"]/text()').extract_first()
        item['level'] = int(response.xpath(
            '//span[@class="MAvaLevel flt1"]/a/@title').extract_first().split('.')[-1])
        if item['level'] <= 3:
            return
        item['tags'] = response.xpath(
            '//div[@class="its_tags"]//i[contains(@class, "on")]/../@title').extract()
        item['attention'] = [int(i) for i in response.xpath(
            '//div[@class="MAvaMore clearfix"]//a/text()').extract()]
        item['groups'] = response.xpath(
            '//div[@class="MGroupDetail"]//a[@class="name"]/text()').extract()
        item['dynamic'] = response.xpath(
            '//span[@class="time"]/text()').extract()
        item['download'] = []
        infos = response.xpath('//div[@class="common_block relative_info"]/p')
        for info in infos:
            if u'刚刚下载了' in ''.join(info.xpath('text()').extract()):

                item['download'].append({'time': info.xpath(
                    'span[@class="time"]/text()').extract_first(), 'name': info.xpath('a/text()').extract()[-1]})

        item['note'] = {}
        item['path'] = []
        item['review'] = []
        item['together'] = []
        note = response.xpath(u'//a[@title="TA的游记"]/@href').extract_first()
        req = Request(urljoin(response.url, note), callback=self.parse_note)
        req.meta['item'] = item
        yield req

    def parse_note(self, response):
        item = response.meta['item']

        item['note']['count'] = response.xpath(
            '//div[@class="MAvaMore clearfix"]//a/text()').extract()
        item['note']['artices'] = []
        for note in response.xpath('//div[@class="notes_list"]//li'):
            article = {'title': note.xpath('.//div[@class="note_info"]/h3/a/text()').extract_first(),
                       'content': note.xpath('.//div[@class="note_word"]/text()').extract_first().strip(),
                       'publish_datetime': note.xpath('.//span[@class="time"]/text()').extract_first(),
                       'read_count': note.xpath('.//span[@class="MInfoNum"]/em')}
            counter = note.xpath(
                './/span[@class="MInfoNum"]/em/text()').extract()
            article['read_count'] = int(counter[0].split('/')[0])
            article['comment_count'] = int(counter[0].split('/')[1])
            article['star_count'] = int(counter[1])

            item['note']['artices'].append(article)
        path = response.xpath(u'//a[@title="TA的足迹"]/@href').extract_first()

        req = Request(urljoin(response.url, path), callback=self.parse_path)
        req.meta['item'] = item
        yield req

    def parse_path(self, response):
        item = response.meta['item']
        for country in response.xpath('//div[@class="country-block other-block"]'):
            for city in country.xpath('div')[1:]:
                path = {}
                path['country'] = ''.join(country.xpath(
                    './/div[@class="cb-hd"]/h2/text()').extract()).strip()
                path['date'] = city.xpath(
                    './/span[@class="time"]/span/text()').extract_first().replace('.', '-')
                path['city'] = city.xpath('.//h3/span/text()').extract_first()
                if not path['city']:
                    path['city'] = city.xpath('.//div[@class="vertical"]/p/text()').extract_first()[:-3]
                path['pois'] = city.xpath('.//h4/text()').extract()
                item['path'].append(path)
        review = response.xpath(u'//a[@title="TA的点评"]/@href').extract_first()
        req = Request(urljoin(response.url, review),
                      callback=self.parse_review)
        req.meta['item'] = item
        yield req

    def parse_review(self, response):
        item = response.meta['item']
        if not response.xpath('//div[@class="no_data"]'):
            for div in response.xpath('//div[@id="_j_poilist"]/div'):
                poi = {}
                poi['name'] = div.xpath(
                    './/h3[@class="title"]/a/text()').extract_first()
                poi['comment'] = div.xpath(
                    './/div[@class="poi-rev _j_comment"]/text()').extract_first().strip()
                poi['comment_datetime'] = div.xpath(
                    './/span[@class="time"]/text()').extract_first().strip()
                poi['star'] = int(
                    div.xpath('.//div[@class="review-score"]/span/@class').extract_first()[-1])
                item['review'].append(poi)

        together = response.xpath(u'//a[@title="TA的结伴"]/@href').extract_first()
        req = Request(urljoin(response.url, together),
                      callback=self.parse_together)
        req.meta['item'] = item
        yield req

    def parse_together(self, response):
        item = response.meta['item']
        for tr in response.xpath('//tr[@class="self"]'):
            together = {}
            together['name'] = ''.join(
                tr.xpath('.//h3//text()').extract()).strip()
            together['from'] = tr.xpath(
                './/td[@class="departure"]/text()').extract_first()
            together['to'] = tr.xpath(
                './/td[@class="destination"]/text()').extract_first().strip()
            together['date'] = tr.xpath(
                './/td[@class="date"]/text()').extract_first()
            together['date'] = together['date'].replace(
                u'月', '-').replace(u'日', '-')
            together['publish_datetime'] = tr.xpath(
                './/div[@class="time _j_time"]/text()').extract_first().strip()
            counter = tr.xpath('.//span[@class="count"]/text()').extract()
            together['read_count'] = int(counter[0])
            together['reply_count'] = int(counter[1])
            item['together'].append(together)
        return item

