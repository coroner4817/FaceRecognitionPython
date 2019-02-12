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

out_test_folder = './out_test/'

def postHandler(meta, embeddings, dscale, mark_face):
  meta_dst = out_test_folder + meta.timestamp + '_meta.csv'
  img_out_dst = out_test_folder+meta.filename
  img_ori_dir = meta.filepath+meta.filename

  with open(meta_dst, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow([meta.timestamp, meta.filepath, meta.filename])
    for i in range(len(embeddings)):
      writer.writerow([str(i), (embeddings[i][1].left()*dscale, embeddings[i][1].top()*dscale, embeddings[i][1].right()*dscale, embeddings[i][1].bottom()*dscale), embeddings[i][0]])

  # TODO: upload image and meta to server
  copyfile(img_ori_dir, img_out_dst)
  if mark_face:
    im = PIL.Image.open(img_out_dst)
    draw = ImageDraw.Draw(im)
    for eb in embeddings:
      draw.rectangle((eb[1].left()*dscale, eb[1].top()*dscale, eb[1].right()*dscale, eb[1].bottom()*dscale), outline=(255,0,0))
    im.save(img_out_dst)

  # delete original image and meta
  os.remove(img_ori_dir)
  # os.remove(meta_dst)



  
