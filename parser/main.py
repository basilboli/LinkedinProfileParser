# -*- coding: utf-8 -*-
# Writen by me, Vasyl Vaskul <basilboli@gmail.com>

import subprocess
import httplib
import urllib2
import simplejson as json
from bottle import route, run, error,request
from crawler import LinkedinCrawler, BadFormatError, PageNotFoundError

@route('/doparse')
def parse():
    url = request.GET.get('url')
    print "Request parameters: url=",url
    if not url:
        return error(PageNotFoundError())

    return parse_url(url)

@error(404)
def error404(error):
    return error(PageNotFoundError())

def parse_url(url):

    if get_status_code(url)==404: # page is not found
        return error(PageNotFoundError())

    output = {}
    crawler = LinkedinCrawler()

    try:
        items = crawler.start(url) # launching crawler
    except BadFormatError:
        return error(BadFormatError())

    output["tags"]= [elem.get('label') for elem in items if 'label' in elem.keys()]# formatting output
    output["educations"] = [elem for elem in items if 'school' in elem.keys()]    
    return json.dumps(output)

def error (error,message=""):
    if (isinstance(error,BadFormatError)):
        return get_error_message(3,"Bad Format of the page")
    elif (isinstance(error,PageNotFoundError)):
        return get_error_message(2,"Page not found. Check whether there is url parameter")
    else:
        return get_error_message(0,"Unknown error")

def get_error_message(error_code,message):
    return json.dumps({"error":{"message":message,"code": error_code}})

def get_status_code(url):
    try:
        connection = urllib2.urlopen(url)
        connection.close()
        return connection.getcode()
    except urllib2.HTTPError, e:
        return e.getcode()

run(host='localhost', port=8081)
