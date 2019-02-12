# hold the message queue which is thread-safe by default (https://docs.python.org/2/library/queue.html)

# this should also including camera control: start/stop

# thread for input_monitor: keep scan the target file dir
#         once there is a new file(tracked using a dict), then push to the message queue, non block
#         scan rate is sync with the actual camera video frame dump rate
#         if the item in the queue is larger than a threshold then raise alarm

# thread pool for data_handler, each thread in the pool will actively looks for item in the sync queue. then process it with dlib

# the data processing will yield [time stamp, img file name, face location, embedding]
# this info will dump to a csv file in the output folder.

# after processing the file, will updload to the server and delete the file and clear the dict cache

# note that this module doesn't require to copy files which will save a lot of time

# if found a thread is blocked then will exit(0)

from input_monitor import InputMonitor
from ThreadBaseClass import ThreadBaseClass, GlobalContext
from data_handler import DataHandler

class Controller(object):
  ThreadBaseClassList = []

  def __init__(self):
    self.mGC = GlobalContext()

    self.mInputMonitor = InputMonitor(self.mGC, 'InputMonitor')
    self.ThreadBaseClassList.append(self.mInputMonitor)

    self.mDataHandler = DataHandler(self.mGC, 'DataHandler')
    self.ThreadBaseClassList.append(self.mDataHandler)

  def setConfig(self, detection_model, landmarks_model, verbose, poolsize, data_folder, file_ext, scan_rate, mark_face):
    self.mInputMonitor.setConfig(data_folder, file_ext, scan_rate)
    self.mDataHandler.setConfig(detection_model, landmarks_model, verbose, poolsize, mark_face)
    pass

  def startUp(self):
    # start all the ThreadBaseClass
    for t in self.ThreadBaseClassList:
      t.start()

  def cleanUp(self):
    # only join the pool when exit 
    # self.mGC.msgQueue.join()
    for t in self.ThreadBaseClassList:
      t.stop()
  
  def logInfo(self):
    print '<HeartBeat CurrQueue: %s, ProcessedCnt: %s, ErrorCnt: %s, AvgProcessTime: %s, HighestProcessTime: %s>' % (str(self.mGC.msgQueue.qsize()), str(self.mGC.processedCnt), str(self.mGC.errorCnt), str(self.mGC.avgProcessTime), str(self.mGC.highestProcessTime))

  def isHealth(self):
    pass
  
