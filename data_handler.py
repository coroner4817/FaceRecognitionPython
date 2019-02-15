import face_recognition_mod.api as face_recognition
from ThreadBaseClass import ThreadBaseClass, GlobalContext
from multiprocessing.pool import ThreadPool
from threading import current_thread
import time
import PIL.Image
import numpy as np
from PostHandler import postHandler


class DataHandler(ThreadBaseClass):

  def setConfig(self, dm, lm, v, ps, mf, ds, ph):
    self.detection_model = dm
    self.landmarks_model = lm
    self.verbose = v
    self.poolsize = ps
    self.mark_face = mf
    self.downsampling_scale = ds
    self.post_handle = ph

  def start(self):
    super(DataHandler, self).start()
    self.pool = ThreadPool(self.poolsize)
    self.pool.map_async(self.run, range(self.poolsize))
  
  def run(self, id):
    print 'Start ThreadPool ' + str(current_thread())
    handle = None
    while self.isAlive:
      time.sleep(0.01)
      if self.gc.msgQueue.qsize() == 0:
        continue

      try:
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
        
        t0 = time.clock()
        self.gc.timeTrackDict[id] = t0
        self.gc.currProcessing[id] = handle.filepath + handle.filename

        # TODO: figure out which downsample resample filter
        # also detection and recognition which is more critical
        # might use downsample for detection and use original image for recognition
        unknown_image, t_load, t_preProc = face_recognition.load_image_file(handle.filepath + handle.filename, dscale=self.downsampling_scale)
        # Scale down image if it's giant so things run a little faster
        # if max(unknown_image.shape) > 1600:
        #   pil_img = PIL.Image.fromarray(unknown_image)
        #   pil_img.thumbnail((1600, 1600), PIL.Image.LANCZOS)
        #   unknown_image = np.array(pil_img)
        unknown_encodings, t_detect, t_recog = face_recognition.face_encodings(unknown_image, None, 1, self.landmarks_model, self.detection_model)

        # post handler
        t_post = time.clock()
        if self.post_handle:
          postHandler(handle, unknown_encodings, self.downsampling_scale, self.mark_face)
          self.gc.fileSet.remove(handle.filename)
        t_post = time.clock() - t_post

        ptime = time.clock() - t0
        if self.verbose > 1:
          print '(Thread id: %s, Face: %s, OverallTime: %s, Load: %s, PreProc: %s, Detection: %s, Recognition: %s, PostHandle: %s)' % (str(id), str(len(unknown_encodings)), str(ptime), str(t_load), str(t_preProc), str(t_detect), str(t_recog), str(t_post))
        self.gc.avgProcessTime = (self.gc.avgProcessTime*(self.gc.processedCnt-1)+ptime)/(float)(self.gc.processedCnt)
        if ptime > self.gc.highestProcessTime:
          self.gc.highestProcessTime = ptime
      except Exception as e:
        if self.verbose > 1:
          print 'A error happened: ' + e + ' Continue handling...'
        self.gc.errorCnt = self.gc.errorCnt + 1
        
      self.gc.timeTrackDict[id] = -1

    print 'Stop ThreadPool ' + str(current_thread())
  
  def stop(self):
    super(DataHandler, self).stop()
    self.pool.close()
    self.pool.join()