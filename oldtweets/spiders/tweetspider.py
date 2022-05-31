import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from oldtweets.items import OldtweetsItem


class TweetSpider(CrawlSpider):
    name = 'oldtweets'
    icounter = 0
    allowed_domain = ['propublica.org']
    start_urls = ['https://projects.propublica.org/politwoops/user/realDonaldTrump?page=1&per_page=50']

    def parse(self, response):
        self.icounter += 1
        if self.icounter > 10:
            raise CloseSpider('ItemExceeded')

        _data = OldtweetsItem()
        # XPATHS
        _xpath_siguiente = '//*[@id="pager"]/div[1]/a[11]/@href'
        _xpath_content = '//div[@class="content"]'

        _t_title = '//h4[@class="tweetTitle"]/a/text()'
        _t_handle = '/html/body/div[3]/div/div/div/div[3]/div[1]/div[1]/div[2]/h4/span/a'
        _t_text = '//p[@class="tweet-text"]'
        _t_deleted = '//div[@class="byline"]'

        for tweet in response.xpath(_xpath_content):
            _data['title'] = tweet.xpath(_t_title).extract()
            _data['handle'] = tweet.xpath(_t_handle).extract()
            _data['text'] = tweet.xpath(_t_text).extract()
            _data['deleted'] = tweet.xpath(_t_deleted).extract()
            yield _data.load_item()

        next_page = response.xpath(_xpath_siguiente).get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
