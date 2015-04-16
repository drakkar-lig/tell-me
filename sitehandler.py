import urllib2
from bs4 import BeautifulSoup

class StackOverflowHandler:
  base = 'https://stackoverflow.com/questions/'

  def get_details_for_question(self,question_id):
    # we use the html page (no usage limitations)
    html = urllib2.urlopen(self.base+str( question_id))
    soup = BeautifulSoup(html)
    question_html=soup.find_all('div',{'class':'post-text'})
    return question_html[0].renderContents(), question_html[1:]

class SiteHandler:

  answers=[]
  index=0
  question_id=0

  def __init__(self,engine="stackoverflow"):
    print engine
    if engine=="stackoverflow":
      self.handler=StackOverflowHandler()
    else:
      raise ValueError("This site is not supported")

  def get(self,question_id):
    if self.index==0 or question_id!=self.question_id:
      self.question,self.answers = self.handler.get_details_for_question(question_id)
      self.index=0
      self.question_id=question_id
    elif self.index>=len(self.answers):
      return 0
    question_html=self.question
    answer_html=self.answers[self.index].renderContents()
    self.index+=1
    return question_html, answer_html
    
