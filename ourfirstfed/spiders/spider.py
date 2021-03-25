import scrapy

from scrapy.loader import ItemLoader

from ..items import OurfirstfedItem
from itemloaders.processors import TakeFirst


class OurfirstfedSpider(scrapy.Spider):
	name = 'ourfirstfed'
	start_urls = ['https://www.ourfirstfed.com/why-first-fed/community/news']

	def parse(self, response):
		post_links = response.xpath('//a[@class="card__action-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="entry-title"]/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]|//div[@class="pf-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//li[@class="datestamp"]/text()').get()

		item = ItemLoader(item=OurfirstfedItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
