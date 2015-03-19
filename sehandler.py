import json
import urllib,urllib2
from BeautifulSoup import BeautifulSoup
import re

class GoogleAPIHandler:
  base = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&'
  queryparam = 'q'
  link=[]
  index=0

  def search(self,site,question):
    if self.index==0:
      question = "site:"+site+" "+" ".join(question)
      query = urllib.urlencode({self.queryparam : question})
      response = urllib2.urlopen(self.base + query).read()
      datajson = json.loads(response)
      for result in datajson['responseData']['results']:
        self.link.append(result["url"])
    elif self.index>=len(self.link):
      return 0

    question_id=[ int(word) for word in self.link[self.index].split('/') if word.isdigit() ][0]
    self.index+=1
    return question_id


class GoogleSearchHandler:
  base = 'https://www.google.com/search?btnG=Google+Search&inurl=https&'
  queryparam = 'q'
  link=[]
  index=0

  def search(self,site,question):
    if self.index==0:
      question = "site:"+site+" "+" ".join(question)
      query = urllib.urlencode({self.queryparam : question})
      opener = urllib2.build_opener()
      opener.addheaders = [('User-agent', 'Mozilla/5.0')]
      response = opener.open(self.base + query).read()
      soup = BeautifulSoup(response)
      anchors = soup.find(id='search').findAll('a')
      for a in anchors:
        if site in a['href']:
          if "webcache" not in a['href'] and "q=related" not in a['href']:
            self.link.append(a['href'])
    elif self.index>=len(self.link):
      return 0
    question_id=[ int(word) for word in self.link[self.index].split('/') if word.isdigit() ][0]
    self.index+=1
    return question_id




class SearchEngineHandler:

  def __init__(self,engine="google"):
    print engine
    if engine=="google":
      self.handler=GoogleSearchHandler()
    elif engine=="googleapi":
      self.handler=GoogleAPIHandler()
    else:
      raise ValueError("This search engine is not supported")

  def search(self,site,question):
    question_id= self.handler.search(site,question)
    return question_id
