import scrapy
from scrapy.utils import log
import sys, os
from crawlyangmodel.items import YangModelItem
from xym import xym

root_url = "https://datatracker.ietf.org"

class IetfMainPageSpider(scrapy.Spider):
    name = "ietf-yang"
    allowed_domains = ["ietf.org"]
    start_urls = [
        "https://datatracker.ietf.org/wg/"
    ]

    def parse(self, response):
        self.logger.info("ready to parse ietf main page")
        area_names = response.css("h2").xpath("text()").extract()
        areas = response.css(".table-condensed")
        wg_params_list = []
        for index,value in enumerate(areas):
            for index2, wg_item in enumerate(value.xpath("tbody/tr")):
                wg_name = wg_item.xpath("td[3]/text()").extract()[0]
                wg_relative_link = wg_item.xpath("./td[1]/a/@href").extract()[0]
                args = {
                        "url"       : root_url + wg_relative_link,
                        "callback"  : self.parse_wg_page,
                        "meta"      : {"area":area_names[index], "wg":wg_name}
                }
                wg_params_list.append(args)

        for index, wg in enumerate(wg_params_list):
            self.logger.info(" WG scrawl, progress [%d/%d] " % (index+1, len(wg_params_list)))
            yield scrapy.Request(**wg)

    def parse_wg_page(self, response):
        self.logger.info("---> parse workgroup page")
        self.logger.info(" the wg url is %s" % (response.url))
        self.logger.info(" workgroup name: %s" % (response.meta['wg']))
        tables = response.css(".table-condensed")
        artifact_param_list = []
        for index, table in enumerate(tables):
            artifacts = table.xpath("tbody/tr")
            for index, artifact in enumerate(artifacts):
                condition = artifact.xpath("td[3]/span[2]/span/text()").extract()
                if ( len(condition) > 0 and condition[0] == u"\u262f"):
                    short_url = artifact.xpath("td[2]/div/a/@href").extract()[0]
                    name = artifact.xpath("td[2]/div/b/text()").extract()[0]
                    self.artifact_name = name
                    args = {
                            "url"       : root_url+short_url,
                            "callback"  : self.parse_artifact_page,
                            "meta"      : {"area": response.meta["area"], "wg":response.meta["wg"], "model_name": name}
                    }

                    artifact_param_list.append(args)

        for index, artifact in enumerate(artifact_param_list):
            self.logger.info(" artifact for WG, progress [%d/%d]" % (index+1, len(artifact_param_list)))
            self.logger.info(" the target url %s" % (artifact['url']))
            yield scrapy.Request(**artifact)

    def parse_artifact_page(self, response):
        self.logger.info("===> parse artifacts...")
        self.logger.info("area:%s, wg:%s, model_name:%s" %(response.meta['area'], response.meta['wg'], response.meta['model_name']))
        url = None
        for i in [4,5,6]:
            text = response.css("table").xpath("tbody/tr[%d]/td[2]/a[1]/text()" %(i)).extract()
            if (len(text) == 0 or "".join(text).strip().find("plain text") == -1):
                continue
            links = response.css("table").xpath("tbody/tr[%d]/td[2]/a[1]/@href" %(i)).extract()
            if (len(links) != 0):
                url = links[0]
                break

        args = {
                "url"       : url,
                "callback"  : self.parse_artifact,
                "meta"      : {"area":response.meta["area"],"wg":response.meta["wg"],"title":response.meta["model_name"]}
        }

        if url is not None:
            yield scrapy.Request(**args)
        else:
            print "no available url for further parsing(area:%s,wg:%s)" %(response.meta['area'], response.meta['wg'])
        #return YangModelItem(**args)

    def parse_artifact(self, response):
        self.logger.info("ready to extract yang model from url: %s" %(response.url))
        content = response.body.splitlines(True)

        if not os.path.exists('./yang-files'):
            os.makedirs('./yang-files')

        ye = xym.YangModuleExtractor(response.url, "./yang-files", strict=False,
                                     strict_examples=False, debug_level=0)
        ye.extract_yang_model(content)
        extracted_yang = ye.get_extracted_models()

        if (len(extracted_yang) == 0):
            self.logger.warning("extracted module from <%s> is empty" %(response.url))
        else:
            print("extracted yang model: [%s]" %(",".join(extracted_yang)))

        # the yield is used to allow scrapy to save meta to a file.
        meta = {
            "area" : response.meta['area'],
            "wg"   : response.meta['wg'],
            "title": response.meta['title'],
            "url"  : response.url,
            "yangs": extracted_yang
        }

        yield meta
