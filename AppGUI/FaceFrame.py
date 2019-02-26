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

  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.master = master

    self.imageLabel = Label(self)
    self.renderLabelImage('./assets/empty_face.JPG')
    self.imageLabel.pack(side=TOP)

    self.textLabel = Label(self)
    self.textLabelvar = StringVar()
    self.textLabel['textvariable'] = self.textLabelvar
    self.textLabelvar.set('No Data')
    self.textLabel.pack(side=BOTTOM)

  def setNewData(self, faceMeta):
    self.renderLabelImage(faceMeta.filepath)
    self.textLabelvar.set(faceMeta.timestamp)

  def renderLabelImage(self, path):
    load = Image.open(path)
    load = load.resize((FACE_IMG_SZ, FACE_IMG_SZ))
    img = ImageTk.PhotoImage(load)
    self.imageLabel.configure(image=img)
    self.imageLabel.image = img
  
