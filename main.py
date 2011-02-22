'''
Created on Feb 22, 2011

@author: awyvw
'''

import time
from webspider import webspider
from webparser import webparser

def main(url):
    ws = webspider()
    ws.setProxy('10.235.96.250', 'axdsp', 'wel57come')
    
    count = 1
    totalpage = 0
    while (url != None):
        page = ws.getpagebyurl(url)
        wp = webparser('taobao', page) 
        wp.parsepage()
        url = wp.getnext()
        print "== Parse Page %d finished ==" % count

        if (wp.hastotalpage == False):
            totalpage = wp.gettotalpagenumber()
            
        if (count < totalpage): 
            count = count + 1
            time.sleep(10)
        else : break


if __name__ == '__main__':
    url = 'http://shopsearch.taobao.com/browse/shop_search.htm?sort=ratesum_desc&shopf=newsearch&q=ipad'
    main(url)