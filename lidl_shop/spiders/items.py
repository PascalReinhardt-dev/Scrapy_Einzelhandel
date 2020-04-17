# -*- coding: utf-8 -*-
import scrapy


class ItemsSpider(scrapy.Spider):
	name = 'items'
	allowed_domains = ['https://www.lidl.de']
	start_urls = ['https://www.lidl.de/de/search?query=*/']

	def parse(self, response):
		for x in response.css('div > ul > li.product-grid__item '):
			item = {
			'Artikelbezeichnung': x.css('span > strong::text').extract(),
			'Anzahl_Bewertungen': x.css('span > div.ratings > span > span >b::text').extract(),
			'Preis_Eur':  x.css('div.pricelabel__integer::text').extract(),
			'Preis_Cent': x.css('div.pricelabel__decimal-superscript::text').extract()
			}
			yield item


		next_page_url = response.css('a.paging-next::attr(href)').extract()
		next_page_url = str(next_page_url)
		next_page_url = next_page_url[2:-2]
		print(next_page_url)

		if next_page_url:
			next_page_url = response.urljoin(next_page_url)
			yield scrapy.Request(url=next_page_url, callback=self.parse,dont_filter=True)

