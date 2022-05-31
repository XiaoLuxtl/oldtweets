import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from oldtweets.items import OldtweetsItem
from w3lib.html import remove_tags


class TweetSpider(CrawlSpider):
    name = 'oldtweets2'
    icounter = 0
    allowed_domain = ['propublica.org']
    start_urls = ['https://projects.propublica.org/politwoops/user/realDonaldTrump?page=1&per_page=50']

    # XPATHS
    _xpath_siguiente = '//a[@class="next_page"]'
    # _xpath_content = '//div[@class="content"]'
    _xpath_content = '//div[@class="permalink"]/a'

    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=_xpath_siguiente)),
        Rule(LinkExtractor(allow=(), restrict_xpaths=_xpath_content),
             callback='parse_item', follow=False)
    }

    def parse_item(self, response, **kwargs):
        # self.icounter += 1
        # if self.icounter > 10:
        #     raise CloseSpider('ItemExceeded')

        _data = OldtweetsItem()

        # XPATHS
        _t_title = '//h4[@class="tweetTitle"]/a/text()'
        _t_handle = '//a[@class="accountHandle linkUnderline"]/text()'
        _t_text = '//p[@class="tweet-text"]'
        _t_deleted = '//div[@class="byline"]'

        _data['title'] = response.xpath(f'normalize-space({_t_title})').extract()
        _data['handle'] = response.xpath(f'normalize-space({_t_handle})').extract()

        _tmp_val = response.xpath(f'normalize-space({_t_text})').extract()
        _tmp_val = remove_tags(str(_tmp_val))
        _tmp_val = _tmp_val.replace("['", '')
        _tmp_val = _tmp_val.replace('["', '')
        _tmp_val = _tmp_val.replace("']", '')
        _tmp_val = _tmp_val.replace('"]', '')
        _data['text'] = remove_tags(str(_tmp_val))

        _tmp_val = response.xpath(f'normalize-space({_t_deleted})').extract()
        _tmp_val = remove_tags(str(_tmp_val))
        _tmp_val = _tmp_val.split('.cls')[0]
        _tmp_val = _tmp_val.replace("['", '')
        _data['deleted'] = remove_tags(str(_tmp_val))

        yield _data

