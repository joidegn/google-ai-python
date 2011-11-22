#!/usr/bin/env python


class Logger:
  def __init__(self):
    global f
    f = open('logger.log', 'w') 

  def log(self,text):
      f.write(repr(text))

