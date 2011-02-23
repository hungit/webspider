'''
Created on Feb 22, 2011

@author: awyvw
'''

import time
from webspider import webspider
from webparser import webparser
from browser import mybrowser

def main(url):
    ws = webspider()
    mb = mybrowser()
    
    #ws.setProxy('10.235.96.250', 'axdsp', 'wel57come')
    mb.setProxy('10.235.96.250:8080', 'axdsp', 'wel57come')
    mb.setCookie()
    mb.setbrowseroptions()
    mb.setagent()
    
    count = 1
    totalpage = 0
    hastotalpage = False
    while (url != None):
        #page = ws.getpagebyurl(url)
        #page = ws.getpagebyurlwithheader(url)
        page = mb.getpagebyurl(url)
        wp = webparser('taobao', page) 
        wp.parsepage()
        url = wp.getnext()
        print "== Parse Page %d finished ==" % count

        #if (hastotalpage == False):
        (totalpage, hastotalpage) = wp.gettotalpagenumber()
            
        if (count < totalpage): 
            count = count + 1
            time.sleep(10)
        else : break


if __name__ == '__main__':
    url = 'http://shopsearch.taobao.com/browse/shop_search.htm?sort=ratesum_desc&shopf=newsearch&q=ipad'
    main(url)