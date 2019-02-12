import threading
import time
from ThreadBaseClass import ThreadBaseClass
import os

class MonitorDog(ThreadBaseClass):

  def setConfig(self, thresh):
    self.timeout = thresh

  def start(self):
    super(MonitorDog, self).start()
    t = threading.Thread(target=self.run, name='monitor_dog_thd', args=())
    t.start()
    self.threadList.append(t)
  
  def run(self):
    while self.isAlive:
      time.sleep(self.timeout)
      tnow = time.clock()
      for t in self.gc.timeTrackDict:
        if self.gc.timeTrackDict[t] != -1:
          if (tnow - self.gc.timeTrackDict[t]) > self.timeout:
            print '[Warning] A thread is blocked, delete this file and wait for restart: %s, delete %s' % (str(tnow - self.gc.timeTrackDict[t]), self.gc.currProcessing[t])
            os.remove(self.gc.currProcessing[t])
            os._exit(1)