import scrapy
import sys, os

from xym import xym

root_url = "https://datatracker.ietf.org"

class IetfMainPageSpider(scrapy.Spider):
    name = "ietf-main-page"
    allowed_domains = ["ietf.org"]
    start_urls = [
        "https://datatracker.ietf.org/wg/"
    ]

    def parse(self, response):
        area_names = response.css("h2").xpath("text()").extract()
        print "\n".join(area_names)
        wgs = []

        areas = response.css(".table-condensed")
        for index,value in enumerate(areas):
            print("area:", area_names[index])
            for index2, wg_item in enumerate(value.xpath("tbody/tr")):
                wg_name = wg_item.xpath("td")[2].xpath("text()").extract()[0]
                wg_relative_link = wg_item.xpath("./td")[0].xpath("./a/@href").extract()[0]
                sys.stdout.write("{:<4}{:<25}{:<20}\n".format(index,  wg_name, wg_relative_link))
                yield scrapy.Request(root_url+wg_relative_link, self.parse_wg_page)
        #return wgs

    def parse_wg_page(self, response):
        #import pdb; pdb.set_trace()
        tables = response.css(".table-condensed")
        for index, table in enumerate(tables):
            artifacts = table.xpath("tbody/tr")
            for index, artifact in enumerate(artifacts):
                condition = artifact.xpath("td[3]/span[2]/span/text()").extract()
                if ( len(condition) > 0 and condition[0] == u"\u262f"):
                    short_url = artifact.xpath("td[2]/div/a/@href").extract()[0]
                    name = artifact.xpath("td[2]/div/b/text()").extract()[0]
                    yield scrapy.Request(root_url+short_url, self.parse_artifact_page)

    def parse_artifact_page(self, response):

        links = response.css("table").xpath("tbody/tr[6]/td[2]/a[1]/@href").extract()
        if (len(links) == 0) :
            #for I-D draft
            links = response.css("table").xpath("tbody/tr[5]/td[2]/a[1]/@href").extract()
        yield scrapy.Request(links[0], self.parse_artifact)
            
                    
    def parse_artifact(self, response):
        print("----->", response.url)
        with open("./tmp.txt","wb+") as file:
            file.write(response.body)
            file.flush()
        
        xym.xym("tmp.txt","./","./", True, True, 2)
        os.remove("./tmp.txt")





