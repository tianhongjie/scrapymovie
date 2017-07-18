import scrapy


class DoubanMovie2Spider(scrapy.Spider):
    name = "douban_movie_100"

    headler = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/56.0.2924.87 '
                      'Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/webp,*/*;q=0.8'
    }

    start_urls = [
        'https://www.douban.com/doulist/13704241/'
    ]

    def __init__(self, *args, **kwargs):
        super(DoubanMovie2Spider, self).__init__(*args, **kwargs)
        if kwargs.get('start_url'):
            self.start_urls = [kwargs.get('start_url')]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse,
                headers=self.headler)

    def parse(self, response):
        for quote in response.css('div.doulist-item'):

            # Just sam as in page
            map_keys = [
                '电影名',
                '评分',
                '类型',
                '主演',
                '年份',
                '制片国家/地区',
                '导演'
            ]

            item = dict.fromkeys(map_keys)
            item.update(
                {
                    "电影名": quote.css(
                        'div.mod div.title a::text').extract_first(),
                    "评分": quote.css(
                        'div.mod span.rating_nums::text').extract_first(),
                    "引言": quote.css(
                        'div.abstract::text').extract()
                }
            )

            # The result is not good
            new_dict = dict(
                map(lambda x: x.split(':'), map(str.strip, item['引言'])))
            item.update(new_dict)
            del (item['引言'])

            # Format the result
            for k, v in item.items():
                if '/' in v:
                    item[k] = list(map(str.strip, v.split('/')))
                else:
                    item[k] = v.strip()
            yield item
        next_url = response.css(
            'div.paginator span.next a::attr(href)').extract_first()
        if next_url:
            yield scrapy.Request(next_url, headers=self.headler)
