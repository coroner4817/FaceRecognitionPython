import threading
import time
from Queue import Queue

MAX_QUEUE_SIZE = 15

class GlobalContext(object):
  msgQueue = Queue(MAX_QUEUE_SIZE)
  fileSet = set()
  processedCnt = 0
  errorCnt = 0
  avgProcessTime = 0
  highestProcessTime = 0
  timeTrackDict = dict()
  currProcessing = dict()

  def __init__(self):
    pass

class ThreadBaseClass(object):
  gc = None

  def __init__(self, glc, name):
    self.gc = glc
    self.name = name
    self.isAlive = True
    self.threadList = []
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