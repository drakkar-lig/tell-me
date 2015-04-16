#!/usr/bin/env python

#import urllib, urllib2, sys, json, gzip, os, time, re
#from bs4 import BeautifulSoup
#from StringIO import StringIO
import sys
from sehandler import SearchEngineHandler
from sitehandler import SiteHandler
from renderer import Renderer


#def ask_google(site,question):
#
#    question = "site:"+site+" "+" ".join(question)
#
#    base = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&'
#    query = urllib.urlencode({'q' : question})
#    response = urllib.urlopen(base + query).read()
#    datajson = json.loads(response)
#    question_url = datajson['responseData']['results'][0]['url']
#
#    question_id=[ int(word) for word in question_url.split('/') if word.isdigit() ][0]
#    return question_id

#def get_details_for_question(question_id):
#    # we use the html page (no usage limitations)
#    html = urllib2.urlopen('http://stackoverflow.com/questions/%d' % question_id)
#    soup = BeautifulSoup(html)
#    question_html=soup.find_all('div',{'class':'post-text'})
#    #print question_html[0]
#    #print question_html[1]
#    #feed_entries = soup.find_all('entry')
#    ## 1st entry is the question
#    #question_html = feed_entries[0].summary.string
#    ## remaining entries are answers
#    #answers_per_rank = { int(entry.find('re:rank').string) : \
#    #        entry.summary.string for entry in feed_entries[1:] }
#    return question_html[0].renderContents(), question_html[1:]



#print question_id
#query="https://api.stackexchange.com/2.2/questions/"+str(question_id)+"?order=desc&site=stackoverflow&filter=withbody"
#print query
#
#request = urllib2.Request(query)
#request.add_header('Accept-encoding', 'gzip')
#response = urllib2.urlopen(request)
#if response.info().get('Content-Encoding') == 'gzip':
#      buf = StringIO( response.read())
#      f = gzip.GzipFile(fileobj=buf)
#      data = f.read()
#
#datajson=json.loads(data)
#question=datajson["items"][0]["body"]
#
#backoff=0
#quota=0
#if "backoff" in datajson:
#  backoff=datajson["backoff"]
#if "quota_remaining" in datajson:
#  quota=datajson["quota_remaining"]
#
#if quota==0:
#  exit(-1)
#
#if backoff>0:
#  time.sleep()
#
#query="https://api.stackexchange.com/2.2/questions/"+str(question_id)+"/answers?order=desc&sort=votes&site=stackoverflow&filter=withbody"
#
#request = urllib2.Request(query)
#request.add_header('Accept-encodng', 'gzip')
#response = urllib2.urlopen(request)
#if response.info().get('Content-Encoding') == 'gzip':
#      buf = StringIO( response.read())
#      f = gzip.GzipFile(fileobj=buf)
#      data = f.read()
#
#
#datajson=json.loads(data)
#print datajson
#answer = datajson["items"][0]["body"]
#
#backoff=0
#quota=0
#if "backoff" in datajson:
#  backoff=datajson["backoff"]
#if "quota_remaining" in datajson:
#  quota=datajson["quota_remaining"]
#
#if quota==0:
#  exit(-1)
#
#if backoff>0:
#  time.sleep()


searchHandler=SearchEngineHandler("google")
siteHandler=SiteHandler("stackoverflow")
question=0
while question!=1:
  question_id=searchHandler.search("stackoverflow.com",sys.argv[1:])
  print question_id
  
  #p = Popen(['pandoc','-s','-f', 'html', '-t','man'],stdin=PIPE,stdout=PIPE)
  
  answer=0
  while answer!=1:

    question, answer = siteHandler.get(question_id)
    renderer=Renderer(question,answer)
    renderer.render()
    #input_html = \
    #            '<div><b>' + QUESTION_INTRODUCTION_LINE +'</b></div>' + \
    #            '<div><b>' + re.sub('.', '-', QUESTION_INTRODUCTION_LINE) + '</b></div>' + \
    #             question + \
    #            '<p></p>' + \
    #            '<p></p>' + \
    #            '<div><b>' + ANSWER_INTRODUCTION_LINE + '</b></div>' + \
    #            '<div><b></b></div>' + re.sub('.', '-', ANSWER_INTRODUCTION_LINE) + '</b></div>' + \
    #             answer
    
    
    
    #sdout=p.communicate(input_html) #.replace(".PP",".HP"))

    #p2 = Popen(['groffer','--mode','tty'],stdin=PIPE)
    #p2.communicate(sdout[0])
    #p2.wait()
    print "Are you satisfied?"
    check=0
    while check!=1:
      ans = raw_input("(y) yes, (q) question was wrong, (a) answer was wrong : ")
      if ans=="q": 
        check=1;answer=1
        print "Trying next question"
      elif ans=="y":
        check=1; question=1;answer=1
      elif ans=="a":
        check=1;
      else:
        print "Please reply y, q or a"
        

    #p2 = Popen(['groffer', '--mode', 'tty'],stdin=PIPE)
    #p2.communicate(toto[0]) #.replace(".PP",".HP"))
    
    #p2 = Popen(['groffer','--mode','tty'],stdin=PIPE)  
    #p2.communicate(toto[0].replace(".PP",".HP"))
    
    
    
