import mechanize
import cookielib

class mybrowser:
    def __init__(self):
        # Init Browser
        self.br = mechanize.Browser()
        
    def setCookie(self):
        cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(cj)
    
    def setProxy(self, proxy, user, password):
        self.br.set_proxies({
            "http": proxy,
        })
        self.br.add_proxy_password(user, password)
        
    def setbrowseroptions(self):
        self.br.set_handle_equiv(True)
        #self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        
    def opendebugmessage(self):
        self.br.set_debug_http(True)
        self.br.set_debug_redirects(True)
        self.br.set_debug_responses(True)
        
    def setagent(self):
        self.br.addheaders = [
            ('User-agent', 
             'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    
    def getpagebyurl(self, url):
        page = self.br.open(url).read()
        page = unicode(page, 'gb2312', 'ignore').encode('utf-8', 'ignore')
        
        print 'Get page by url via browser successful'
        return page
      