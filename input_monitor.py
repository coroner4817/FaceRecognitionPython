import os
import threading
import time
from ThreadBaseClass import ThreadBaseClass
from MetaData import MetaData
import cv2

CAM_NAME = 0

class InputMonitor(ThreadBaseClass):

  def setConfig(self, df, fe, sr, uc):
    self.data_folder = df
    self.file_extension = fe
    self.scan_rate = sr
    self.use_camera = uc
    if self.use_camera:
      self.cap = cv2.VideoCapture(CAM_NAME)

  def start(self):
    super(InputMonitor, self).start()
    t = threading.Thread(target=self.run, name='input_scan_thd', args=())
    t.start()
    self.threadList.append(t)

  def run(self):
    while self.isAlive:
      if self.use_camera and self.cap.isOpened():
        ret, frame = self.cap.read()
        if ret:
          # dump to file
          fname = time.strftime("%H-%M-%S")+self.file_extension
          cv2.imwrite(self.data_folder+fname, frame)
          # new obj push to queue and set
          self.gc.fileSet.add(fname)
          msg = MetaData(self.data_folder, fname)
          self.gc.msgQueue.put(msg)
        cv2.waitKey(self.scan_rate * 1000)
      else:
        time.sleep(self.scan_rate)
        # check the file list
        for f in os.listdir(self.data_folder):
          if f.endswith(self.file_extension) and f not in self.gc.fileSet:
            # new obj push to queue and set
            self.gc.fileSet.add(f)
            msg = MetaData(self.data_folder, f)
            self.gc.msgQueue.put(msg)

  def stop(self):
    super(InputMonitor, self).stop()
    if self.use_camera: 
      self.cap.release()
    
