from elasticsearch import Elasticsearch
from elasticsearch import helpers


class page_rank_crawl:

    def __init__(self):
        self.cloud_id = "9b1128ec78574fcd91ae19ac14496c8b:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRjYzY0MmMyMjQxNmQ0NzVjYmI1OTdiZmJiMjFmNTlhNCQ4ZjkxY2UzNjVlODk0NWVkYjc2YmY0NDQzZTMwMjhlNg=="
        self.index = "mass_gov"
        self.es = Elasticsearch(request_timeout=10000, cloud_id=self.cloud_id, http_auth=('elastic', "rFE1RkD1dJr54MPCtHaFHqub"))
        self.inlinks = {}
        self.outlinks = {}



    def get_inlinks(self):
        all_docs = helpers.scan(self.es,
                                index=self.index,
                                query={
                                    "query": {
                                        "match_all": {}
                                    },
                                    "_source": ["inlinks"]
                                },
                                size=2000,
                                request_timeout=30)
        count = 0
        for i in all_docs:
            count += 1
            print(count)
            url = i["_id"]
            #print("url",url)
            inlinks = i["_source"]["inlinks"]
            #print('inlinks :',inlinks)
            self.inlinks[url] = inlinks


    def write_inlinks(self):
        with open("crawled_links/crawled_inlinks.txt", "a") as f:
            for url in self.inlinks:
                line = "{} ".format(url)
                for l in self.inlinks[url]:
                    line += "{} ".format(l)
                f.write(line)
                f.write("\n")



    def get_outlinks(self):
        all_docs = helpers.scan(self.es,
                                index=self.index,
                                query={
                                    "query": {
                                        "match_all": {}
                                    },
                                    "_source": ["outlinks"]
                                },
                                size=2000,
                                request_timeout=30)
        count = 0
        for i in all_docs:
            count += 1
            print(count)
            url = i["_id"]
            outlinks = i["_source"]["outlinks"]
            self.outlinks[url] = outlinks



    def write_outlinks(self):
        with open("crawled_links/crawled_outlinks.txt", "a", encoding="utf-8") as f:
            for url in self.outlinks:
                line = "{} ".format(url)
                for l in self.outlinks[url]:
                    line += "{} ".format(l)
                f.write(line)
                f.write("\n")


es = page_rank_crawl()
es.get_inlinks()
es.write_inlinks()
es.get_outlinks()
es.write_outlinks()

