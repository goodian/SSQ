# coding=utf-8
import urllib2
import re
import time
from selenium import webdriver

OUT_FILE = "./result.txt"

URL = "http://zx.caipiao.163.com/trend/ssq_historyPeriod.html"

CUR = 114

JOU_MAP = {2003 : 89,
           2004 : 123,
           2005 : 154,
           2006 : 154,
           2007 : 154,
           2008 : 154,
           2009 : 154,
           2010 : 153,
           2011 : 153,
           2012 : 154,
           2013 : 154,
           2014 : CUR,
           }

def http_request_get(url):
    if not url or len(url):
        print "http_request_get err: url is None"
    h = urllib2.Request(url)
    ht = urllib2.urlopen(h)
    html = ht.read(ht)
    return html
#end http_request_get

def get_value(pat, string):
    if not string or len(string) == 0:
        print "get value err: string is None"
        return (None, "")
    if pat == None:
        print "get value err: pat is None"
        return (None, "")

    k = re.search(pat, string)
    if k == None:
        return (None, "")
    return (k.group(1), string[k.end():])

def parse_request(html):
    if not html:
        return
    title_pat = "<td align=\"center\" title=\".*\">(\d{7})"
    rq_pat = "<td class=\"c_ba2636\">(\d{2})</td>"
    bq_pat = "<td class=\"c_1e50a2\">(\d{2})</td>"
    while True:
        (title, html) = get_value(title_pat, html)
        if title:
            (rq0, html) = get_value(rq_pat, html)
            (rq1, html) = get_value(rq_pat, html)
            (rq2, html) = get_value(rq_pat, html)
            (rq3, html) = get_value(rq_pat, html)
            (rq4, html) = get_value(rq_pat, html)
            (rq5, html) = get_value(rq_pat, html)
            (bq0, html) = get_value(bq_pat, html)
            print [title, rq0, rq1, rq2, rq3, rq4, rq5, bq0]
        else:
            break
    #end for
#end parse_request

if __name__ == '__main__':
    for year in JOU_MAP.keys():
        url = "%s?beginPeriod=%d001&endPeriod=%d%d" % (URL, year, year, JOU_MAP[year])
        print url
        html = http_request_get(url)
        parse_request(html)
