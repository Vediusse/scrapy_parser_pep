import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org/"]

    def parse(self, response):
        for table in response.css("table"):
            all_peps = table.css("td:nth-child(2) > a::attr(href)")
            for pep_link in all_peps:
                yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response: scrapy.http.Response):
        pep_number, pep_name = (
            response.css("h1.page-title::text").get().split(" – ")
        )
        pep_number = pep_number.replace("PEP ", "")
        data = {
            "number": pep_number,
            "name": pep_name,
            "status": response.css("dt:contains('Status') + dd ::text").get(),
        }
        print(data)
        yield PepParseItem(data)
