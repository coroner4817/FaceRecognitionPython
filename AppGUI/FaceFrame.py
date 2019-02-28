from Tkinter import *
from PIL import Image, ImageTk

FACE_IMG_SZ = 70

################
#
#    Image
#  
#    Labels
#

class FaceFrame(Frame):

  def __init__(self, master=None, isSuspectFace=False):
    Frame.__init__(self, master)
    self.master = master
    self.isSuspectFace = isSuspectFace

    self.imageLabel = Label(self)
    self.renderLabelImage('./assets/empty_face.JPG')
    self.imageLabel.pack(side=TOP)

    # time label
    self.textLabel = Label(self)
    self.textLabelvar = StringVar()
    self.textLabel['textvariable'] = self.textLabelvar
    self.textLabelvar.set('No Data')
    self.textLabel.pack(side=BOTTOM)

    # name label
    if isSuspectFace:
      self.textLabelName = Label(self)
      self.textLabelNamevar = StringVar()
      self.textLabelName['textvariable'] = self.textLabelNamevar
      self.textLabelNamevar.set('No Data')
      self.textLabelName.pack(side=BOTTOM)

  def setNewData(self, faceMeta):
    if len(faceMeta.timestamp) > 8:
      faceMeta.timestamp = faceMeta.timestamp[:8]
    if len(faceMeta.suspect_name) > 8:
      faceMeta.suspect_name = faceMeta.suspect_name[:8]
    self.renderLabelImage(faceMeta.filepath)
    self.textLabelvar.set(faceMeta.timestamp)
    if self.isSuspectFace:
      self.textLabelNamevar.set(faceMeta.suspect_name)

  def renderLabelImage(self, path):
    load = Image.open(path)
    load = load.resize((FACE_IMG_SZ, FACE_IMG_SZ))
    img = ImageTk.PhotoImage(load)
    self.imageLabel.configure(image=img)
    self.imageLabel.image = img
  
