#!/usr/bin/env python

import urllib, urllib2, sys, json
from bs4 import BeautifulSoup
from StringIO import StringIO
import gzip
import os
from subprocess import Popen, PIPE, STDOUT
import time

question = "site:stackoverflow.com "+" ".join(sys.argv[1:])

base = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&'
query = urllib.urlencode({'q' : question})
response = urllib.urlopen(base + query).read()
datajson = json.loads(response)
question_url = datajson['responseData']['results'][0]['url']

question_id=[ int(word) for word in question_url.split('/') if word.isdigit() ][0]

#print question_id
query="https://api.stackexchange.com/2.2/questions/"+str(question_id)+"?order=desc&site=stackoverflow&filter=withbody"
print query

request = urllib2.Request(query)
request.add_header('Accept-encoding', 'gzip')
response = urllib2.urlopen(request)
if response.info().get('Content-Encoding') == 'gzip':
      buf = StringIO( response.read())
      f = gzip.GzipFile(fileobj=buf)
      data = f.read()

datajson=json.loads(data)
question=datajson["items"][0]["body"]

backoff=0
quota=0
if "backoff" in datajson:
  backoff=datajson["backoff"]
if "quota_remaining" in datajson:
  quota=datajson["quota_remaining"]

if quota==0:
  exit(-1)

if backoff>0:
  time.sleep()

query="https://api.stackexchange.com/2.2/questions/"+str(question_id)+"/answers?order=desc&sort=votes&site=stackoverflow&filter=withbody"

request = urllib2.Request(query)
request.add_header('Accept-encoding', 'gzip')
response = urllib2.urlopen(request)
if response.info().get('Content-Encoding') == 'gzip':
      buf = StringIO( response.read())
      f = gzip.GzipFile(fileobj=buf)
      data = f.read()


datajson=json.loads(data)
#print datajson
answer = datajson["items"][0]["body"]

backoff=0
quota=0
if "backoff" in datajson:
  backoff=datajson["backoff"]
if "quota_remaining" in datajson:
  quota=datajson["quota_remaining"]

if quota==0:
  exit(-1)

if backoff>0:
  time.sleep()

#p = Popen(['w3m','-T', 'text/html','-dump'],stdin=PIPE)  
#p.communicate(question+"<p>-------<b>toto</b>-----------</p>"+answer)
p = Popen(['pandoc','-f', 'html', '-t','groff'],stdin=PIPE,stdout=PIPE)  
toto=p.communicate(question+"<p>-------<b>toto</b>-----------</p>"+answer)
print toto[0]
groff=""
p2 = Popen(['less'],stdin=PIPE)  
p2.communicate(toto[0].replace(".PP",".HP"))

#p2 = Popen(['groffer','--mode','tty'],stdin=PIPE)  
#p2.communicate(toto[0].replace(".PP",".HP"))
