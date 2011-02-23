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
    
    ws.setProxy('10.235.96.250', 'axdsp', 'wel57come')
    mb.setProxy('10.235.96.250:8080', 'axdsp', 'wel57come')
    mb.setCookie()
    mb.setbrowseroptions()
    mb.setagent()
    
    linklist = []
    # get shop cat list
    catlist = getshoplistbybrowser(mb, url)
    # parse shop list one by one   
    for item in catlist:
        linklist.append(parseshoplistbybrowser(mb, item))
        break
    
    # get shop rate link list
    for item in linklist:
        for rate in item:
            for detail in rate:
                parseshopratedetailbybrowser(mb, detail)

def getshoplistbybrowser(mb, url):
    page = mb.getpagebyurl(url)
    wp = webparser('taobao', page)
    catlist = wp.parseproductcat()
    
    return catlist

def parseshoplistdirect(ws, url):
    count = 1
    totalpage = 0
    hastotalpage = False
    while (url != None):
        #page = ws.getpagebyurl(url)
        page = ws.getpagebyurlwithheader(url)
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

def parseshoplistbybrowser(mb, url):
    count = 1
    totalpage = 0
    hastotalpage = False
    ratelinklist = []
    while (url != None):
        page = mb.getpagebyurl(url)
        wp = webparser('taobao', page) 
        wp.parsepage()
        url = wp.getnext()
        ratelinklist.append(wp.ratelinklist)
        #if (hastotalpage == False):
        (totalpage, hastotalpage) = wp.gettotalpagenumber()
        print "== Parse Page %d finished ==" % count
                   
        if (count < totalpage): 
            count = count + 1
            time.sleep(10)
        else : break
        
        break
        
    return ratelinklist

def parseshopratedetailbybrowser(mb, url):
    page = mb.getpagebyurl(url)
    wp = webparser('rate information', page)
    wp.parseproductratedetail(wp.soup)
    print "== Parse rate information finished =="

if __name__ == '__main__':
    #url = 'http://shopsearch.taobao.com/browse/shop_search.htm?sort=ratesum_desc&shopf=newsearch&q=ipad'
    url = 'http://jie.taobao.com/'
    main(url)