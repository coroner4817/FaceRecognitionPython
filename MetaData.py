# data class to hold meta info 
import os

class MetaData(object):
  timestamp = None
  filepath = None  # parent path
  filename = None

  def __init__(self, fp, fn, em=None, fb=None):
    self.filepath = fp
    self.filename = fn
    self.timestamp = os.path.splitext(self.filename)[0]
    
  def __str__(self):

    return '<TimeStamp: %s, FilePath: %s>' % (self.timestamp, self.filepath+self.filename)

