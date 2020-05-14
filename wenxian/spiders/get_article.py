# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import WenxianItem
import requests
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

class GetArticleSpider(scrapy.Spider):
    name = 'get_article'
    allowed_domains = ['sci-hub.tw']
    start_urls = ['https://sci-hub.tw/']
    doi_str = input('输入网址，以英文,隔开：')
    dois = doi_str.split(',')


    def get_name(self, doi):
        res = requests.get(doi, headers=headers).content
        selector = etree.HTML(res)
        if 'pubs.acs.org' in doi:
            name = selector.xpath("//h1[@class='article_header-title']/span[@class='hlFld-Title']/text()")[0].strip()
        elif 'wiley.com' in doi:
            name = selector.xpath("//h1[@class='citation__title']/text()")[0].strip()
        elif 'sciencedirect.com' in doi:
            name = selector.xpath("//span[@class='title-text']/text()")[0].strip()
        elif 'pubs.rsc.org' in doi:
            name = selector.xpath("//h2[@class='capsule__title fixpadv--m']/text()")[0].strip()
        elif 'nature.com' in doi:
            name = selector.xpath("//h1[@class='c-article-title u-h1']/text()")[0].strip()
        elif 'sciencemag.org' in doi:
            name = selector.xpath("//div[@class='highwire-cite-title']/text()")[0].strip()
        else:
            name = None
        return name

    def start_requests(self):
        for doi in self.dois:
            url = 'https://sci-hub.tw/'+doi
            name = self.get_name(doi)
            request = scrapy.Request(url, callback=self.parse, meta={'name':name})
            yield request

    def parse(self, response):
        download_url = 'https:'+response.xpath("//iframe[@id='pdf']/@src").get()
        download_url = re.search(r'(.+)#.+',download_url).group(1)
        name = response.meta['name']
        if not name:
            name = re.search(r'.+?/downloads/.+?/.+?/(.+?\.pdf)', download_url)
            name = name.group(1)
        else:
            name = name + '.pdf'
        print(name)
        item = WenxianItem(
            file_urls=[download_url],
            name=name
        )
        yield item
