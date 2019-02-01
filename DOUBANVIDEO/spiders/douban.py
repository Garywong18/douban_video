# -*- coding: utf-8 -*-
import scrapy
from DOUBANVIDEO.items import DoubanvideoItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    base_url = 'https://movie.douban.com/top250?start={}&filter='
    page = 1
    start_urls = [base_url.format((page-1)*25)]

    def parse(self, response):
        video_list = response.xpath("//ol[@class='grid_view']/li")
        for video in video_list:
            item = DoubanvideoItem()
            #name = video.xpath("//div[@class='hd']/a/span[1]/text()").extract_first()
            item['name'] = video.xpath("./div//div[@class='hd']/a/span[1]/text()").extract_first()
            item['tag'] = video.xpath("./div//div[@class='bd']/p/text()").extract()
            item['point'] = video.xpath(".//span[@class='rating_num']/text()").extract_first()
            item['slogn'] = video.xpath(".//span[@class='inq']/text()").extract_first()
            yield item

        self.page += 1
        if self.page == 11:
            return
        url = self.base_url.format((self.page-1)*25)
        yield scrapy.Request(
            url,
            callback=self.parse
        )





