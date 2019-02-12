import threading
import time
from Queue import Queue

class GlobalContext(object):
  msgQueue = Queue()
  fileSet = set()
  processedCnt = 0
  errorCnt = 0
  avgProcessTime = 0
  highestProcessTime = 0

  def __init__(self):
    pass

class ThreadBaseClass(object):
  gc = None
  isAlive = True
  threadList = []
  name = None

  def __init__(self, glc, name):
    self.gc = glc
    self.name = name
    pass
  
  def start(self):
    print 'start ThreadBaseClass: ' + self.name
    # is inHerit class' responibility to add the thread to the threadlist
    pass
  
  def run(self):
    pass

  def stop(self):
    print 'stop ThreadBaseClass: ' + self.name
    self.isAlive = False
    for t in self.threadList:
      if t.isAlive():
        t.join()