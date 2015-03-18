#!/usr/bin/env python

import urllib, urllib2, sys, json
from bs4 import BeautifulSoup
from StringIO import StringIO
import gzip
import os
from subprocess import Popen, PIPE, STDOUT

question = "site:stackoverflow.com "+" ".join(sys.argv[1:])

base = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&'
query = urllib.urlencode({'q' : question})
response = urllib.urlopen(base + query).read()
datajson = json.loads(response)
question_url = datajson['responseData']['results'][0]['url']

question_id=[ int(word) for word in question_url.split('/') if word.isdigit() ][0]

#print question_id
query="https://api.stackexchange.com/2.2/questions/"+str(question_id)+"?order=desc&site=stackoverflow&filter=withbody"

request = urllib2.Request(query)
request.add_header('Accept-encoding', 'gzip')
response = urllib2.urlopen(request)
if response.info().get('Content-Encoding') == 'gzip':
      buf = StringIO( response.read())
      f = gzip.GzipFile(fileobj=buf)
      data = f.read()

datajson=json.loads(data)
question=datajson["items"][0]["body"]

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

#p = Popen(['w3m','-T', 'text/html','-dump'],stdin=PIPE)  
#p.communicate(question+"<p>-------<b>toto</b>-----------</p>"+answer)
p = Popen(['pandoc','-f', 'html', '-t','man'],stdin=PIPE,stdout=PIPE)  
toto=p.communicate(question+"<p>-------<b>toto</b>-----------</p>"+answer)
groff=""
p2 = Popen(['groffer','--mode','tty'],stdin=PIPE)  
p2.communicate(toto[0])

