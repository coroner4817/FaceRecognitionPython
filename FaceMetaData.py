
class FaceMetaData(object):
  id = None
  timestamp = None
  filepath = None
  isSuspect = None

  def __init__(self, i, ts):
    self.id = i
    self.timestamp = ts
    self.filepath = ''
    self.isSuspect = False

  def __str__(self):
    return '<FaceMeta: %s, TimeStamp: %s, FilePath: %s, isSuspect: %s>' % (str(self.id), self.timestamp, self.filepath, str(self.isSuspect))
