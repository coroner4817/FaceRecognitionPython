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
import face_recognition_mod.api as face_recognition
import numpy as np
import cv2

out_test_folder = './out_test/'

def compareFaceLocal():
  # TODO:
  pass

def postHandler(meta, embeddings, dscale, mark_face, dist_thresh, local_suspect_list):
  meta_dst = out_test_folder + meta.timestamp + '_meta.csv'
  img_out_dst = out_test_folder + meta.filename
  img_ori_dir = meta.filepath + meta.filename
  face_map = dict()

  # TODO: upload image and meta to server
  # block call
  copyfile(img_ori_dir, img_out_dst)
  if len(embeddings) == 0:
    return face_map, img_out_dst

  embeddings = zip(range(len(embeddings)), embeddings)

  with open(meta_dst, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow([meta.timestamp, meta.filepath, meta.filename])
    for eb in embeddings:
      writer.writerow([str(eb[0]), (eb[1][1].left()*dscale, eb[1][1].top()*dscale, eb[1][1].right()*dscale, eb[1][1].bottom()*dscale), eb[1][0]])
      face_map[eb[0]] = FaceMetaData(eb[0], meta.timestamp)

  # TODO: assume get the sync recogition info
  if len(local_suspect_list) > 0:
    for eb in embeddings:
      dist = face_recognition.face_distance(eb[1][0], zip(*local_suspect_list)[1])
      min_index = dist.argmin()
      if dist[min_index] < dist_thresh:
        face_map[eb[0]].isSuspect = True
        face_map[eb[0]].suspect_name = local_suspect_list[min_index][0]

  if mark_face:
    # im = PIL.Image.open(img_out_dst)

    # for eb in embeddings:
    #   cropped = im.crop((eb[1][1].left()*dscale, eb[1][1].top()*dscale, eb[1][1].right()*dscale, eb[1][1].bottom()*dscale))
    #   path = out_test_folder + meta.timestamp + '_crop_' + str(eb[0]) + '.JPG'
    #   cropped.save(path)
    #   face_map[eb[0]].filepath = path

    # draw = ImageDraw.Draw(im)
    # for eb in embeddings:
    #   draw.rectangle((eb[1][1].left()*dscale, eb[1][1].top()*dscale, eb[1][1].right()*dscale, eb[1][1].bottom()*dscale), outline=(255,0,0))
    # im.save(img_out_dst)

    # use opencv
    im = cv2.imread(img_out_dst)

    for eb in embeddings:
      cropped = im[eb[1][1].top()*dscale : eb[1][1].bottom()*dscale, eb[1][1].left()*dscale : eb[1][1].right()*dscale]
      path = out_test_folder + meta.timestamp + '_crop_' + str(eb[0]) + '.JPG'
      cv2.imwrite(path, cropped)
      face_map[eb[0]].filepath = path
    
    for eb in embeddings:
      cv2.rectangle(im, (eb[1][1].left()*dscale, eb[1][1].top()*dscale), (eb[1][1].right()*dscale, eb[1][1].bottom()*dscale), color=(0,0,255), thickness=3)
    cv2.imwrite(img_out_dst, im)

  # TODO: delete meta file and croped face and frame images, delay deletion
  os.remove(meta_dst)

  return face_map, img_out_dst