import scrapy


class DoubanMovieSpider(scrapy.Spider):
    name = "douban_movie"

    headler = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/56.0.2924.87 '
                      'Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/webp,*/*;q=0.8'
    }

    start_urls = [
        'https://movie.douban.com/top250'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse,
                headers=self.headler)

    def parse(self, response):
        for quote in response.css('div.item'):
            yield {
                "电影名": quote.css(
                    'div.info div.hd a span.title::text').extract_first(),
                "评分": quote.css(
                    'div.info div.bd div.star span.rating_num::text').extract(),
                "引言": quote.css(
                    'div.info div.bd p.quote span.inq::text').extract()
            }
        next_url = response.css(
            'div.paginator span.next a::attr(href)').extract()
        if next_url:
            next_url = "https://movie.douban.com/top250" + next_url[0]
            print(next_url)
            yield scrapy.Request(next_url, headers=self.headler)
