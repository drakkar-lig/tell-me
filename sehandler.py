import json
import urllib,urllib2
from BeautifulSoup import BeautifulSoup

class GoogleAPIHandler:
  base = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&'
  queryparam = 'q'

  def search(self,site,question):
    question = "site:"+site+" "+" ".join(question)
    query = urllib.urlencode({self.queryparam : question})
    response = urllib2.urlopen(self.base + query).read()
    datajson = json.loads(response)
    link=[]
    for result in datajson['responseData']['results']:
      link.append(result["url"])
    return link



class GoogleSearchHandler:
  base = 'https://www.google.com/search?btnG=Google+Search&inurl=https&'
  queryparam = 'q'

  def search(self,site,question):
    question = "site:"+site+" "+" ".join(question)
    query = urllib.urlencode({self.queryparam : question})
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(self.base + query).read()
    soup = BeautifulSoup(response)
    anchors = soup.find(id='search').findAll('a')
    link=[]
    for a in anchors:
      if site in a['href']:
        if "webcache" not in a['href'] and "q=related" not in a['href']:
          link.append(a['href'])
    return link




class SearchEngineHandler:

  link=[]
  index=0

  def __init__(self,engine="google"):
    print engine
    if engine=="google":
      self.handler=GoogleSearchHandler()
    elif engine=="googleapi":
      self.handler=GoogleAPIHandler()
    else:
      raise ValueError("This search engine is not supported")

  def search(self,site,question):
    if self.index==0:
      self.link = self.handler.search(site,question)
    elif self.index>=len(self.link):
      return 0
    question_id=[ int(word) for word in self.link[self.index].split('/') if word.isdigit() ][0]
    self.index+=1
    return question_id
    
