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

out_test_folder = './out_test/'

def postHandler(meta, embeddings):
  meta_dst = out_test_folder + meta.timestamp + '_meta.csv'
  with open(meta_dst, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow([meta.timestamp, meta.filepath, meta.filename])
    id = 0
    for i in embeddings:
      writer.writerow([str(id), i[1], i[0]])
      id = id + 1
  
  # TODO: upload image and meta to server
  # copyfile(meta.filepath+meta.filename, out_test_folder+meta.filename)
  # copyfile meta data

  # delete original image and meta
  os.remove(meta.filepath+meta.filename)
  # os.remove(meta_dst)



  
