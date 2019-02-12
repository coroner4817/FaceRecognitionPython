import os
import threading
import time
from ThreadBaseClass import ThreadBaseClass
from MetaData import MetaData


class InputMonitor(ThreadBaseClass):

  def setConfig(self, df, fe, sr):
    self.data_folder = df
    self.file_extension = fe
    self.scan_rate = sr

  def start(self):
    super(InputMonitor, self).start()
    t = threading.Thread(target=self.run, name='input_scan_thd', args=())
    t.start()
    self.threadList.append(t)

  def run(self):
    while self.isAlive:
      time.sleep(self.scan_rate)
      # check the file list
      for f in os.listdir(self.data_folder):
        if f.endswith(self.file_extension) and f not in self.gc.fileSet:
          # new obj push to queue and set
          self.gc.fileSet.add(f)
          msg = MetaData(self.data_folder, f)
          self.gc.msgQueue.put(msg)


    
