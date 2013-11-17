import urllib2
from BeautifulSoup import BeautifulSoup

class Bing(object):

  def __init__(self, term):
    self.term = term
    self.url = "http://www.bing.com/news/search?q=" + self.term
    self.html = BeautifulSoup(urllib2.urlopen(self.url).read())

  def do_search(self):
    div = self.html.body.find('div', attrs={'class':'newstitle'}).a
    text = div.getText()
    url = div.attrs[0][1]

    return (text, url)