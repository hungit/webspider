'''
Created on Feb 22, 2011

@author: awyvw
'''

from BeautifulSoup import BeautifulSoup

ENCODING = 'gb18030'

class webparser:
    def __init__(self, parsername, html):
        self.name = parsername
        self.soup = BeautifulSoup(html)
        self.dict = []
        self.hastotalpage = False
        
    def __del__(self):
        self.name = ''
        
    def getscopbydiv(self, soup, divid=''):
        if divid != '':
            subsoup = soup.find('div', id=divid)
        else:
            subsoup = soup.find('div')
            
        print 'Get top scop by %s' % divid
        return subsoup
        
    def getscopbytagattr(self, soup, tag, attr, val):
        sublist = soup.findAll(tag, {attr : val})
        print "Get sub list by tag: '%s', attr: '%s', value: '%s'" % (tag, attr, val)           
        return sublist
        
    def gettablescop(self, soup, tag):
        subsoup = soup.find(tag)
        print 'Get table scop successful'
        return subsoup
    
    def gettableitem(self, soup, tag):
        list = soup.findAll(tag)
        print 'Get table %s items' % len(list)
        return list
    
    def gettextonly(self, soup):
        v = soup.text
        if v == None:
            cn = soup.contents
            resulttext = ''
            for item in cn:
                subtext = self.gettextonly(item)
                resulttext += subtext + '\n'
            return resulttext.encode(ENCODING)
        else:
            return v.encode(ENCODING)
    
    def parseproductlist(self):
        soup = self.getscopbydiv(self.soup, 'main-content')
        soup = self.gettablescop(soup, 'tbody')
        list = self.gettableitem(soup, 'tr')
        print 'Get product %s item' % len(list)
        count = 1
        for item in list:
            print 'Parsing No. %d item' % count 
            self.parseproductitem(item)
            count = count + 1
        return len(list)
    
    def parseproductitem(self, soup):
        plist = []
        
        list = self.gettableitem(soup, 'td')
        
        if (len(list) < 5): return
        
        # block 1 : product information
        (blc, shopref) = self.parseproductinfo(list[0])
        plist.append(shopref)
        plist.append(blc)
        
        # block 2 : product amount
        blc = self.parseproductamount(list[1])
        plist.append(blc)
        
        # block 4 : product location
        blc = self.parseproductlocation(list[3])
        plist.append(blc)
        
        # block 5 : product rate
        blc = self.parseproductrate(list[4])
        plist.append(blc)
        
        self.dict.append(plist)
    
    def parseproductinfo(self, soup):
        # get shop logo
        link = soup.find('div').find('img')
        if ('src' in dict(link.attrs)):
            print 'image ref : %s' % link['src']
        
        bloc = soup.find('dl')
        # get shop link and name
        link = bloc.find('dt').find('a')
        if ('href' in dict(link.attrs)):
            print 'Shop link : %s' % link['href']
        print 'Shop name : %s' % self.gettextonly(link)
        
        # get shop products
        bloc = soup.find('dd')
        blist = bloc.findAll('p')
        for item in blist:            
            plink = item.find('a')
            if plink != None:
                # get product page link
                if ('href' in dict(plink.attrs)):
                    print 'Product page link : %s' % plink['href']
                print 'Product : %s' % self.gettextonly(plink)
            else:                  
                # get protect information         
                plist = item.findAll('ins')
                for item in plist:
                    if ('title' in dict(item.attrs)):
                        print 'Protect info : %s' % item['title'].encode(ENCODING)
            
        # get cut information
        clist = bloc.find('ul').findAll('li')
        for item in clist:
            print 'cut information : %s' % self.gettextonly(item)
            
        return ('product info', 'product link')
    
    def parseproductamount(self, soup):
        pbloc = soup.find('p')
        # Confirm the class name
        if ('amount' in dict(pbloc.attrs)):
            print 'Product amount : %s' % self.gettextonly(pbloc.contents)
            
        return 'product amount'
    
    def parseproductlocation(self, soup):
        print 'Product location : %s' % self.gettextonly(soup)
        
        return 'product location'
    
    def parseproductrate(self, soup):
        plist = soup.findAll('p')
        for item in plist:
            abloc = item.find('a')
            
            # get shop rank information
            if (('class' in dict(abloc.attrs)) and ('rank' == abloc['class']) and ('href' in dict(abloc.attrs))):
                print '%s :' % self.gettextonly(abloc)
                print '%s' % abloc['href']
                
            # get shop score information
            if (('class' in dict(abloc.attrs)) and ('score' == abloc['class']) and ('data-score' in dict(abloc.attrs))):
                print '%s :' % self.gettextonly(abloc) 
                print '%s' % abloc['data-score']
                
        return 'product rate'
    
    def parsepage(self):
        if self.soup == None:
            print 'There is no html can be parse'
            return
        
        print 'Parse web page...'
        return self.parseproductlist()
                
    def getnext(self):
        souplist = self.getscopbytagattr(self.soup, 'div', 'class', 'page-bottom')
        if len(souplist) < 1 : return None
        
        pagenext = self.getscopbytagattr(souplist[0], 'a', 'class', 'page-next')
        if ((pagenext != None) and (len(pagenext) > 0)):
            if ('href' in dict(pagenext[0].attrs)):
                link = pagenext[0]['href']
                print 'Next url : %s' % link
                return link 
        return None
    
    def gettotalpagenumber(self):
        souplist = self.getscopbytagattr(self.soup, 'div', 'class', 'page-top')
        if (len(souplist) < 1) : return 0
        
        pagenum = self.getscopbytagattr(souplist[0], 'span', 'class', 'page-info')
        if (len(pagenum) < 1) : return 0
        
        print 'Raw total page number info : %s' % pagenum[0].text
        
        numlist = self.gettextonly(pagenum[0]).split('/')
        if (len(numlist) < 1) : return 0
        
        total = int(numlist[1])
        
        print 'Total page number is : %d' % total
        return (total, True)
    