# take place in the pool
# will take care of 
#  - parse and dump data to the meta data file
#  - upload the image and meta data
#  - rm the image file
# the file set is cleaned at the data_handler after post handling

from MetaData import MetaData
import csv
from shutil import copyfile
import os
import PIL
from PIL import ImageDraw
from FaceMetaData import *
import random

out_test_folder = './out_test/'

def compareFaceLocal():
  # TODO:
  pass

def postHandler(meta, embeddings, dscale, mark_face, dist_thresh):
  meta_dst = out_test_folder + meta.timestamp + '_meta.csv'
  img_out_dst = out_test_folder + meta.filename
  img_ori_dir = meta.filepath + meta.filename

  embeddings = zip(range(len(embeddings)), embeddings)
  face_map = dict()

  with open(meta_dst, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow([meta.timestamp, meta.filepath, meta.filename])
    for eb in embeddings:
      writer.writerow([str(eb[0]), (eb[1][1].left()*dscale, eb[1][1].top()*dscale, eb[1][1].right()*dscale, eb[1][1].bottom()*dscale), eb[1][0]])
      face_map[eb[0]] = FaceMetaData(eb[0], meta.timestamp)

  # TODO: upload image and meta to server
  copyfile(img_ori_dir, img_out_dst)
  # TODO: assume get the sync recogition info
  for eb in embeddings:
    face_map[eb[0]].isSuspect = bool(random.getrandbits(1))

  if mark_face:
    im = PIL.Image.open(img_out_dst)

    for eb in embeddings:
      cropped = im.crop((eb[1][1].left()*dscale, eb[1][1].top()*dscale, eb[1][1].right()*dscale, eb[1][1].bottom()*dscale))
      path = out_test_folder + meta.timestamp + '_crop_' + str(eb[0]) + '.JPG'
      cropped.save(path)
      face_map[eb[0]].filepath = path

    draw = ImageDraw.Draw(im)
    for eb in embeddings:
      draw.rectangle((eb[1][1].left()*dscale, eb[1][1].top()*dscale, eb[1][1].right()*dscale, eb[1][1].bottom()*dscale), outline=(255,0,0))
    im.save(img_out_dst)

  # TODO: delete meta file and croped face and frame images, delay deletion
  # os.remove(meta_dst)

  return face_map, img_out_dst