import face_recognition_mod.api as face_recognition
from ThreadBaseClass import ThreadBaseClass, GlobalContext
from multiprocessing.pool import ThreadPool
from threading import current_thread
import time
import PIL.Image
import numpy as np
from PostHandler import postHandler
from AppGUI.AppView import UpdateType
import os


SUSPECT_DATABASE_PATH = './suspects/'

class DataHandler(ThreadBaseClass):
  last_encoding = []

  def setConfig(self, dm, lm, v, ps, mf, ds, ph, ad, dt, fe, ls):
    self.detection_model = dm
    self.landmarks_model = lm
    self.verbose = v
    self.poolsize = ps
    self.mark_face = mf
    self.downsampling_scale = ds
    self.post_handle = ph
    self.avoid_duplicate = ad
    self.distance_thresh = dt
    self.load_suspect = ls
    self.local_suspect_list = []
    if self.load_suspect:
      # load suspect database first, assume each database only have one face
      for f in os.listdir(SUSPECT_DATABASE_PATH):
        if f.endswith(fe):
          if self.verbose > 0: print 'Suspect name: ' + os.path.splitext(f)[0]
          unknown_image, _, _ = face_recognition.load_image_file(SUSPECT_DATABASE_PATH+f, dscale=self.downsampling_scale)
          unknown_encodings, _, _ = face_recognition.face_encodings(unknown_image, None, 1, self.landmarks_model, self.detection_model)
          self.local_suspect_list.append((os.path.splitext(f)[0], unknown_encodings[0][0]))

  def setListener(self, listener):
    self.updateListener = listener

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
        valid_encoding = []
        if self.avoid_duplicate and len(self.last_encoding) > 0:
          for eb in unknown_encodings:
            dist = face_recognition.face_distance(zip(*self.last_encoding)[0], eb[0])
            if np.min(dist) > self.distance_thresh:
              valid_encoding.append(eb)
        else:
          valid_encoding = unknown_encodings
        self.last_encoding = unknown_encodings

        if self.post_handle:
          face_info_dict, stream_path = postHandler(handle, valid_encoding, self.downsampling_scale, self.mark_face, self.distance_thresh, self.local_suspect_list)
          self.updateListener(UpdateType.STREAM, stream_path)
          self.updateListener(UpdateType.DETECTION, face_info_dict)

          # delete cache files
          os.remove(handle.filepath + handle.filename)
          self.gc.fileSet.remove(handle.filename)
          os.remove(stream_path)
          for face in face_info_dict:
            os.remove(face_info_dict[face].filepath)
        t_post = time.clock() - t_post

        ptime = time.clock() - t0
        if self.verbose > 1:
          print '(Thread id: %s, Face: %s, OverallTime: %s, Load: %s, PreProc: %s, Detection: %s, Recognition: %s, PostHandle: %s)' % (str(id), str(len(unknown_encodings)), str(ptime), str(t_load), str(t_preProc), str(t_detect), str(t_recog), str(t_post))
        self.gc.avgProcessTime = (self.gc.avgProcessTime*(self.gc.processedCnt-1)+ptime)/(float)(self.gc.processedCnt)
        if ptime > self.gc.highestProcessTime:
          self.gc.highestProcessTime = ptime

        self.updateListener(UpdateType.META, ["Current Queue: " + str(self.gc.msgQueue.qsize()), "Processed: " + str(self.gc.processedCnt), "Error: " + str(self.gc.errorCnt), "Avg time: " + str(self.gc.avgProcessTime), "Highest time: " + str(self.gc.highestProcessTime)])
      except Exception as e:
        if self.verbose > 0:
          print 'A error happened: ' + e + ' Continue handling...'
        self.gc.errorCnt = self.gc.errorCnt + 1
        
      self.gc.timeTrackDict[id] = -1

    print 'Stop ThreadPool ' + str(current_thread())
  
  def stop(self):
    super(DataHandler, self).stop()
    self.pool.close()
    self.pool.join()