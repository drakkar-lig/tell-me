import json
import urllib,urllib2

class GoogleHandler:
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


class SearchEngineHandler:

  def __init__(self,engine="google"):
    if engine=="google":
      self.handler=GoogleHandler()
    else:
      raise ValueError("This search engine is not supported")

  def search(self,site,question):
    question_id= self.handler.search(site,question)
    return question_id
