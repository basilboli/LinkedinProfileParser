""" tests for the our magic parser """
from nose.tools import *
from linkedinparser.parser.crawler import LinkedinCrawler, BadFormatError, PageNotFoundError
import unittest

def setup():
    print "TEAR UP!"

def teardown():
    print "TEAR DOWN!"

def test_crawler():
	url = "http://www.linkedin.com/in/vasylvaskul"
	crawler = LinkedinCrawler()
	items = crawler.start(url)
	print "items=",items
	assert items
	      
def test_crawler_bad_format():
	url = "http://www.1linkedin.com/in/vasylvaskul"	
	crawler = LinkedinCrawler()	
	try:		
		items = crawler.start(url)	
	except BadFormatError:
		print "items=",items
		print ">>>>>>>>>>>>>>>>>Wrong URL"


	    
