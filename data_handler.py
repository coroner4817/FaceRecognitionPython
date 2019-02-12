import face_recognition_mod.api as face_recognition
from ThreadBaseClass import ThreadBaseClass, GlobalContext
from multiprocessing.pool import ThreadPool
from threading import current_thread
import time
import PIL.Image
import numpy as np
from PostHandler import postHandler


class DataHandler(ThreadBaseClass):

  def setConfig(self, dm, lm, v, ps):
    self.detection_model = dm
    self.landmarks_model = lm
    self.verbose = v
    self.poolsize = ps

  def start(self):
    super(DataHandler, self).start()
    self.pool = ThreadPool(self.poolsize)
    self.pool.map_async(self.run, range(self.poolsize))
  
  def run(self, id):
    print 'Start ThreadPool ' + str(current_thread())
    handle = None
    while self.isAlive:
      if self.gc.msgQueue.qsize() == 0:
        continue

      try:
        t0 = time.clock()
        try:
          # supress racing error
          handle = self.gc.msgQueue.get_nowait()
          if self.verbose > 1:
            print 'Thread id ' + str(id) + ': ' + str(handle)
          self.gc.processedCnt = self.gc.processedCnt + 1
        except:
          continue
        if handle.filename is None:
          continue

        unknown_image = face_recognition.load_image_file(handle.filepath + handle.filename)
        # Scale down image if it's giant so things run a little faster
        if max(unknown_image.shape) > 1600:
          # TODO: downsampling
          pil_img = PIL.Image.fromarray(unknown_image)
          pil_img.thumbnail((1600, 1600), PIL.Image.LANCZOS)
          unknown_image = np.array(pil_img)
        unknown_encodings = face_recognition.face_encodings(unknown_image, None, 1, self.landmarks_model, self.detection_model)

        # post handler
        postHandler(handle, unknown_encodings)
        self.gc.fileSet.remove(handle.filename)

        ptime = time.clock() - t0
        if self.verbose > 1:
          print 'Thread id ' + str(id) + ': ' + 'find ' + str(len(unknown_encodings)) + ' face. Time: ' + str(ptime)
        self.gc.avgProcessTime = (self.gc.avgProcessTime*(self.gc.processedCnt-1)+ptime)/(float)(self.gc.processedCnt)
        if ptime > self.gc.highestProcessTime:
          self.gc.highestProcessTime = ptime
      except:
        if self.verbose > 1:
          print 'A error happened when parsing this file. Continue handling'
        self.gc.errorCnt = self.gc.errorCnt + 1

    print 'Stop ThreadPool ' + str(current_thread())
  
  def stop(self):
    super(DataHandler, self).stop()
    self.pool.close()
    self.pool.join()