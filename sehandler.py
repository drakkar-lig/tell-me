import json
import urllib,urllib2
from BeautifulSoup import BeautifulSoup
import re

class GoogleAPIHandler:
  base = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&'
  queryparam = 'q'

  def search(self,site,question):
    question = "site:"+site+" "+" ".join(question)
    query = urllib.urlencode({self.queryparam : question})
    response = urllib2.urlopen(self.base + query).read()
    datajson = json.loads(response)
    question_url = datajson['responseData']['results'][0]['url']

    question_id=[ int(word) for word in question_url.split('/') if word.isdigit() ][0]
    return question_id

class GoogleSearchHandler:
  base = 'https://www.google.com/search?btnG=Google+Search&inurl=https&'
  queryparam = 'q'


  def search(self,site,question):
    question = "site:"+site+" "+" ".join(question)
    query = urllib.urlencode({self.queryparam : question})
    print self.base+query
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(self.base + query).read()
    soup = BeautifulSoup(response)
    anchors = soup.find(id='search').findAll('a')
    link=[]
    for a in anchors:
      if "stackoverflow.com" in a['href']:
        link.append(a['href'])

    #datajson = json.loads(response)
    #question_url = datajson['responseData']['results'][0]['url']

    question_id=[ int(word) for word in link[0].split('/') if word.isdigit() ][0]
    print question_id
    return question_id

class DuckDuckGoHandler:
  base = 'https://duckduckgo.com/?'
  queryparam = 'q'


  def search(self,site,question):
    question = "site:"+site+" "+" ".join(question)
    query = urllib.urlencode({self.queryparam : question})
    print self.base+query
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(self.base + query).read()
    print response
    soup = BeautifulSoup(response)
    anchors = soup.find(id='search').findAll('a')
    print anchors
    link=[]
    for a in anchors:
      if "stackoverflow.com" in a['href']:
        link.append(a['href'])

    #datajson = json.loads(response)
    #question_url = datajson['responseData']['results'][0]['url']

    question_id=[ int(word) for word in link[0].split('/') if word.isdigit() ][0]
    print question_id
    return question_id

class SearchEngineHandler:

  def __init__(self,engine="google"):
    print engine
    if engine=="google":
      self.handler=GoogleSearchHandler()
    elif engine=="googleapi":
      self.handler=GoogleAPIHandler()
    elif engine=="duckduckgo":
      self.handler=DuckDuckGoHandler()
    else:
      raise ValueError("This search engine is not supported")

  def search(self,site,question):
    question_id= self.handler.search(site,question)
    return question_id
