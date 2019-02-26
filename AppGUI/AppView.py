import threading
from Tkinter import *
from PIL import Image, ImageTk
from enum import Enum
from FaceFrame import *
from FaceMetaData import *

#############################
#                 |
#      stream     | suspect
#                 |
# ---------------------------
#     all face    |   meta
#                 |

class UpdateType(Enum):
  STREAM = 0
  DETECTION = 1 # all and suspect
  META = 2  

ALL_FACE_SIZE = 12
SUSPECT_FACE_SIZE = 4

threadLock = threading.Lock()
# TODO: - delete img file when next img is ready to show
#       - For 4 threads, stream should use a priority queue to maket sure early image comes first
class AppView(object):
  all_face_list = [FaceMetaData(-1, 0)] * ALL_FACE_SIZE
  suspect_face_list = [FaceMetaData(-1, 0)] * SUSPECT_FACE_SIZE * 2

  allFaceFrames = []
  all_index = 0
  suspectFaceFrames = []
  suspect_index = 0

  def __init__(self, r):
    self.root = r
    self.init()

  def setConfig(self, v):
    self.verbose = v

  def init(self):
    # init view
    # stream
    self.streamFrame = Frame(self.root)
    self.streamFrame.grid(column=0, row=0, sticky=(N, W))
    self.streamLabel = Label(self.streamFrame, anchor=W)
    self.streamLabel.pack()
    self.renderLabelImage(self.streamLabel, './assets/empty_stream.JPG')
    
    # all face
    self.all_face_frame = Frame(self.root)
    self.all_face_frame.grid(column=0, row=1, sticky=(N, E))
    for i in range(ALL_FACE_SIZE):
      temp = FaceFrame(self.all_face_frame)
      temp.pack(side=LEFT)
      self.allFaceFrames.append(temp)

    # suspect face
    # self.suspect_face_frame = Frame(self.root)
    # self.suspect_face_frame.grid(column=1, row=0, sticky=(W, S))

    # self.suspect_face_frame1 = Frame(self.suspect_face_frame)
    # self.suspect_face_frame1.pack(side=LEFT)
    # for i in range(SUSPECT_FACE_SIZE):
    #   temp = FaceFrame(self.suspect_face_frame1)
    #   temp.pack(side=BOTTOM)
    #   self.suspectFaceFrames.append(temp)

    # self.suspect_face_frame2 = Frame(self.suspect_face_frame)
    # self.suspect_face_frame2.pack(side=LEFT)
    # for i in range(SUSPECT_FACE_SIZE):
    #   temp = FaceFrame(self.suspect_face_frame2)
    #   temp.pack(side=BOTTOM)
    #   self.suspectFaceFrames.append(temp)

    # self.meta_data_frame = Frame(self.suspect_face_frame)
    # self.meta_data_frame.pack(side=BOTTOM)
    # self.meta_label = Label(self.meta_data_frame, text='Current Queue:\nProcessed:\nError:\nAvg time:\nHighest time:\n')

    self.suspect_face_frame1 = Frame(self.root)
    self.suspect_face_frame1.grid(column=1, row=0, sticky=(W, S))
    for i in range(SUSPECT_FACE_SIZE):
      temp = FaceFrame(self.suspect_face_frame1, True)
      temp.pack(side=BOTTOM)
      self.suspectFaceFrames.append(temp)

    self.suspect_face_frame2 = Frame(self.root)
    self.suspect_face_frame2.grid(column=2, row=0, sticky=(W, S))
    for i in range(SUSPECT_FACE_SIZE):
      temp = FaceFrame(self.suspect_face_frame2, True)
      temp.pack(side=BOTTOM)
      self.suspectFaceFrames.append(temp)

    # meta data
    self.meta_data_frame = Frame(self.root)
    self.meta_data_frame.grid(column=1, row=1, sticky=(E, S))
    self.meta_label = Label(self.root)
    self.meta_label_var = StringVar()
    self.meta_label['textvariable'] = self.meta_label_var
    self.meta_label_var.set('Current Queue:\nProcessed:\nError:\nAvg time:\nHighest time:\n')

    for child in self.root.winfo_children(): child.grid_configure(padx=5, pady=5)

  def renderLabelImage(self, label, path, dscale=1.5):
    load = Image.open(path)
    load.thumbnail((load.size[0]/dscale, load.size[1]/dscale))
    img = ImageTk.PhotoImage(load)
    label.configure(image=img)
    label.image = img

  def onUpdate(self, utype, args):
    # threadLock.acquire()
    if self.verbose > 1:
      print utype, args

    if utype == UpdateType.STREAM:
      self.renderLabelImage(self.streamLabel, args)
    elif utype == UpdateType.DETECTION:
      for a_id in args:
        if args[a_id].isSuspect:
          # self.addFixedSZList(args[a_id], self.suspect_face_list, SUSPECT_FACE_SIZE * 2)
          self.suspect_index = self.updateFaceFrames(self.suspectFaceFrames, self.suspect_index, args[a_id])
        else:
          self.all_index = self.updateFaceFrames(self.allFaceFrames, self.all_index, args[a_id])
      #     self.addFixedSZList(args[a_id], self.all_face_list, ALL_FACE_SIZE)
      # if len(args):
      #   self.updateFaceFrames()
    elif utype == UpdateType.META:
      self.updateMetaData(args)
    # threadLock.release()
  
  def getOnUpdate(self):
    return self.onUpdate

  def addFixedSZList(self, item, a_list, sz):
    if len(a_list) == sz:
      del a_list[0]
    elif len(a_list) < sz:
      pass
    else:
      a_list = alist[:sz]
      del a_list[0]
    a_list.append(item)
  
  def updateFaceFrames(self):
    for i in range(ALL_FACE_SIZE):
      if self.all_face_list[i].id != -1:
        self.allFaceFrames[i].setNewData(self.all_face_list[i])

    for i in range(SUSPECT_FACE_SIZE * 2):
      if self.suspect_face_list[i].id != -1:
        self.suspectFaceFrames[i].setNewData(self.suspect_face_list[i])

  def updateFaceFrames(self, frames, index, meta):
    frames[index].setNewData(meta)
    index = index + 1
    if index == len(frames):
      index = 0
    return index

  def updateMetaData(self, meta):
    s = ''.join(e + '\n' for e in meta)
    self.meta_label_var.set(s)
