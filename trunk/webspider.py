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