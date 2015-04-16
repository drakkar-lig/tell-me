from subprocess import Popen, PIPE, STDOUT
import re

class Renderer:

  engine=['w3m', '-T', 'text/html', '-cols','80','-dump']

  QUESTION_INTRODUCTION_LINE= \
    "The following question seems related to yours:"
  ANSWER_INTRODUCTION_LINE= \
    "And the best answer was:"

  def __init__(self,question_html,answer_html): 
    self.question_html=question_html
    self.answer_html=answer_html
  
  def render(self):
    input_html = \
                '<div><b>' + self.QUESTION_INTRODUCTION_LINE +'</b></div>' + \
                '<div><b>' + re.sub('.', '-', self.QUESTION_INTRODUCTION_LINE) + '</b></div>' + \
                 self.question_html + \
                '<p></p>' + \
                '<p></p>' + \
                '<div><b>' + self.ANSWER_INTRODUCTION_LINE + '</b></div>' + \
                '<div><b></b></div>' + re.sub('.', '-', self.ANSWER_INTRODUCTION_LINE) + '</b></div>' + \
                 self.answer_html
    p1 = Popen(self.engine,stdin=PIPE,stdout=PIPE)
    p1.stdin.write(input_html)
    p2 = Popen(['less'],stdin=p1.stdout)
    p1.stdin.close()
    p2.wait()
