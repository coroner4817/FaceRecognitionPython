import face_recognition_mod.api as face_recognition
from ThreadBaseClass import ThreadBaseClass, GlobalContext
from multiprocessing.pool import ThreadPool
from threading import current_thread
import time
import PIL.Image
import numpy as np
from PostHandler import postHandler

pool_size = 4

class DataHandler(ThreadBaseClass):

  def start(self):
    super(DataHandler, self).start()
    self.pool = ThreadPool(pool_size)
    self.pool.map_async(self.run, range(pool_size))
  
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
        unknown_encodings = face_recognition.face_encodings(unknown_image)

        postHandler(handle, unknown_encodings)

        # post handler
        self.gc.fileSet.remove(handle.filename)
        print 'Thread id ' + str(id) + ': ' + 'find ' + str(len(unknown_encodings)) + ' face. Time: ' + str(time.clock()-t0)
      except:
        print 'A error happened when parsing this file. Continue handling'
        self.gc.errorCnt = self.gc.errorCnt + 1
        # TODO:

    print 'Stop ThreadPool ' + str(current_thread())
  
  def stop(self):
    super(DataHandler, self).stop()
    self.pool.close()
    self.pool.join()