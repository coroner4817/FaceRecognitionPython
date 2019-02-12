import os
import threading
import time
from ThreadBaseClass import ThreadBaseClass
from MetaData import MetaData

scan_rate = 1
data_folder = './captures/'
file_extension = '.JPG'

class InputMonitor(ThreadBaseClass):

  def start(self):
    super(InputMonitor, self).start()
    t = threading.Thread(target=self.run, name='input_scan_thd', args=())
    t.start()
    self.threadList.append(t)

  def run(self):
    while self.isAlive:
      time.sleep(1)
      # check the file list
      for f in os.listdir(data_folder):
        if f.endswith(file_extension) and f not in self.gc.fileSet:
          # new obj push to queue and set
          self.gc.fileSet.add(f)
          msg = MetaData(data_folder, f)
          self.gc.msgQueue.put(msg)


    
