# coding=utf-8
import urllib2
import re, sys
import time
from utils import *

#get data from zhcw.com

DATA_FILE = "./result.txt"

URL = "http://tubiao.zhcw.com/tubiao/ssqNew/ssqInc/ssqZongHeFengBuTuAsckj_year=%s.html"

title_pat = r"<a title=开奖日期：.*>(\d{5})\s*\w*</a>"
rq_pat = "<td class='green5qiu|redqiu.*'>(\d{1,2})</td>"
bq_pat = "<td class='blueqiu3\s*.*'>(\d{1,2})</td>"

CUR_YEAR = 2014

def http_request_get(url):
    if not url or len(url) == 0:
        print "http_request_get err: url is None"
    h = urllib2.Request(url)
    ht = urllib2.urlopen(h)
    html = ht.read()
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
    global out_fp
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
            out_fp.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (title, rq0, rq1, rq2, rq3, rq4, rq5, bq0))
        else:
            break
    #end for
#end parse_request


def get_data_by_year(year=""):
    if not year:
        return

    url = URL % year
    print "Getting data of year: %s" % year
    html = http_request_get(url)
    time.sleep(2)
    parse_request(html)

if __name__ == '__main__':
    out_fp = open_for_write(DATA_FILE)
    if not out_fp:
        print "can not open file: %s, quit" % DATA_FILE
        sys.exit(-1)
    for year in range(2003, CUR_YEAR + 1):
        get_data_by_year(str(year))

    close_file(out_fp)
