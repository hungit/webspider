'''
Created on Feb 22, 2011

@author: awyvw
'''
import urllib2

class webspider(object):
    def setProxy(self, proxy, username, password):
        proxy_support = urllib2.ProxyHandler({'http' : proxy})
        passmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passmgr.add_password(None, proxy, username, password)
        authinfo = urllib2.ProxyBasicAuthHandler(passmgr)
        opener = urllib2.build_opener(proxy_support, authinfo)
        urllib2.install_opener(opener)
        
        print 'Set proxy successful'
    
    def getpagebyurl(self, url):
        self.page = urllib2.urlopen(url)
        page = self.page.read()
        page = unicode(page, 'gb2312', 'ignore').encode('utf-8', 'ignore')
        
        print 'Get page by url successful'
        return page  
    
    def getpagebyurlwithheader(self, url):
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }  
        req = urllib2.Request(url = url, headers = headers)
        
        self.page = urllib2.urlopen(req)
        page = self.page.read()
        page = unicode(page, 'gb2312', 'ignore').encode('utf-8','ignore')
        
        print 'Get page by url like internet explorer successful'
        return page