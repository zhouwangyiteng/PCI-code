# coding:utf-8

import urllib2
from BeautifulSoup import *
from urlparse import urljoin
from pysqlite2 import dbapi2 as sqlite
import re


ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])




class crawler:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)


    def __del__(self):
        self.con.close()


    def dbcommit(self):
        self.con.commit()


    def getentryid(self, table, field, value, creatnew=True):
        cur = self.con.execute("select rowid from %s where %s='%s'"
                               % (table, field, value))
        res = cur.fetchone()
        if res==None:
            cur = self.con.excute("insert into %s (%s) values ('%s')"
                                  % (table, field, value))
            return cur.lastrowid
        else:
            return res[0]


    def addtoindex(self, url, soup):
        if self.isindexed(url):
            return
        print 'Indexing %s' % url

        text = self.gettextonly(soup)
        words = self.separatewords(text)

        urlid = self.getentryid('urllist', 'url', url)

        for i in range(len(words)):
            word = words[i]
            if word in ignorewords:
                continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute('insert into wordlocation(urlid, wordid, location)\
                             values (%d, %d, %d)' % (urlid, wordid, i))


    def gettextonly(self, soup):
        v = soup.string
        if v==None:
            c = soup.contents
            reaulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()


    def separatewords(self, text):
        sqlitter = re.compile('\\W*')
        return [s.lower() for s in sqlitter.split(text) if s!='']


    def isindexed(self, url):
        u = self.con.execute("select rowid from urllist where url='%s'"
                             % url).fetchone()
        if u!=None:
            v = self.con.execute("select * from wordlocation where urlid=%d"
                                 % u[0]).fetchone()
            if v!=None:
                return True
        return False


    def addlinkref(self, urlForm, urlTo, linkText):
        pass


    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:
                try:
                    c = urllib2.urlopen(page)
                except:
                    print "Count not open %s" % page
                    continue
                soup = BeautifulSoup(c.read())
                self.addtoindex(page, soup)

                links = soup('a')
                for link in links:
                    if 'href' in dict(links.attrs):
                        url = urljoin(page, link['href'])
                        if url.find("'")!=-1:
                            continue
                        url = url.split('#')[0]
                        if url[:4]=='http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText = self.gettextonly(link)
                        self.addlinkref(page, url, linkText)
                self.dbcommit()
            page = newpages


    def creatindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid, wordid, location)')
        self.con.execute('create table link(fromid integer, toid integer)')
        self.con.execute('create table linkwords(wordid, linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbcommit()

















    

    
