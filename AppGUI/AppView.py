from Tkinter import *
from PIL import Image, ImageTk
from enum import Enum

#############################
#                 |
#      stream     | suspect
#                 |
# ---------------------------
#   all detectin  |   meta
#                 |

class UpdateType(Enum):
  STREAM = 0
  DETECTION = 1 # all and suspect
  META = 2


class AppView(object):
  def __init__(self, r):
    self.root = r

  def onUpdate(self, utype, args):
    print utype, args

    if utype == UpdateType.STREAM:
      pass
    elif utype == UpdateType.DETECTION:
      pass
    elif utype == UpdateType.META:
      pass
  
  def getOnUpdate(self):
    return self.onUpdate