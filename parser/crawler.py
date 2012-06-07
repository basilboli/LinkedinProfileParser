# -*- coding: utf-8 -*-
# Writen by me, Vasyl Vaskul <basilboli@gmail.com>

import re
import httplib
from scrapy.contrib.loader import XPathItemLoader
from scrapy.item import Item, Field
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy import project, signals
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
from multiprocessing.queues import Queue
from multiprocessing import Process

class BadFormatError(Exception): pass
class PageNotFoundError(Exception): pass

class Education(Item):    
    """linkedin educations"""
    year_first = Field()
    year_last = Field()
    diploma = Field()
    school = Field()
    location = Field()
    speciality = Field()

class Competence(Item):    
    """linkedin competences"""
    label = Field()

class LinkedinSpider(BaseSpider):
    """Our ad-hoc spider of the linkedin public pages"""
    
    def __init__(self, url=None):
        self.url = url
        BaseSpider.__init__(self)
    
    name = "linkedinspider"
    url = ""
    def parse(self, response):
        self.log('A response from %s with code just arrived! ' % response.url)
        items = []
        x = HtmlXPathSelector(response)          
        
        #checking out if the page is proper for parsing 
        if not x.select("//h1/span[@id='name']"):
            return items
        
        #parsing education
        educations= x.select("//div[@id='profile-education']/div[2]/div/div")        
        for education in educations:            
            item = Education()
            item['school'] = re.sub(r'(^\s*|\s*$)','',education.select('h3/text()').extract()[0]).encode("utf-8")# cutting trash before and after
            item['year_first'] = education.select("descendant::*[contains(@class,'dtstart')]/text()").extract()[0]
            item['year_last'] = education.select("descendant::*[contains(@class,'dtend')]/text()").extract()[0]
            items.append(item)                             
        
        #parsing competences
        competences= x.select("//div[@id='profile-skills']/div[contains(@class,'content')]/descendant::a/text()")      
        for competence in competences:            
            item = Competence()
            # pattern=re.compile(r'\s')
            item['label'] = re.sub(r'(^\s*|\s*$)','',competence.extract()).encode("utf-8")# cutting trash before and after
            items.append(item)                                 

        return items
    
    def start_requests(self):
        return [Request(self.url, callback=self.parse)]

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        pass

class CrawlerWorker(Process):
    def __init__(self, spider, results):
        Process.__init__(self)
        self.results = results

        self.crawler = CrawlerProcess(settings)
        if not hasattr(project, 'crawler'):
            self.crawler.install()
        self.crawler.configure()

        self.items = []
        self.spider = spider
        dispatcher.connect(self._item_passed, signals.item_passed)

    def _item_passed(self, item):
        self.items.append(item)

    def run(self):
        self.crawler.crawl(self.spider)        
        self.crawler.start()
        self.crawler.stop()
        self.results.put(self.items)

class CrawlerScript():

    def __init__(self, spider, results):
        self.results = results
        self.crawler = CrawlerProcess(settings)
        if not hasattr(project, 'crawler'):
            self.crawler.install()
        self.crawler.configure()
        self.items = []
        self.spider = spider
        dispatcher.connect(self._item_passed, signals.item_passed)

    def _item_passed(self, item):
        self.items.append(item)

    def run(self):
        self.crawler.crawl(self.spider)
        self.crawler.start()
        self.crawler.stop()
        self.results.put(self.items)


class LinkedinCrawler:  
    """
    We are using scrapy inline e.g. using CrawlerWorker.    
    It's also possible to instantiate scrapy using subprocess.For ex :      
    cmd="scrapy crawl linkedin"
    output = subprocess.check_output("scrapy crawl linkedin -o out.json -t json && cat out.json",shell=True)
    output = subprocess.check_output("scrapy crawl linkedin -o stdout: -t json",shell=True)
    subprocess.Popen('echo "Hello world!"', shell=True)
    """ 
  
    def start(self,url):                
        # raise BadFormatError
        items = []
        # The part below can be called as often as you want        
        results = Queue()
        crawler = CrawlerWorker(LinkedinSpider(url), results)
        crawler.start()
        for item in results.get():
            items.append(dict(item))
        return items