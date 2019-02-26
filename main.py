import signal
import sys
import time
import getopt
import click

from controller import Controller
pc = Controller()
isActive = True

from AppGUI.AppView import *
from Tkinter import *
root = Tk()
view = AppView(root)

def updateLoop():
  pc.logInfo()
  root.after(3000, updateLoop)

def on_close():
  pc.cleanUp()
  isActive = False
  sys.exit(0)

@click.command()
@click.option('--detection_model', default="hog", help='Available models: "hog", "cnn", "cnn" is more accurate but slow and might yield error')
@click.option('--landmarks_model', default="large", help='Available models: "small", "large", "large" is using 68 landmarks points')
@click.option('--verbose', default=1, help='verbose level 0-2')
@click.option('--poolsize', default=1, help='ThreadPool size base on CPU number. Recommand 4')
@click.option('--data_folder', default='./captures/', help='Data folder for searching for input files')
@click.option('--file_ext', default='.JPG', help='Image file extension of the camera output')
@click.option('--scan_rate', default=2, help='How long to sleep before next file scan, should match camera dump rate')
@click.option('--mark_face', default=True, type=bool, help='If set to True will draw a bounding box on the output , to use GUI must turn on this flag')
@click.option('--thread_timeout', default=0, help='Set the timeout for processing time of thread pool. If set to 0 then is not monitored')
@click.option('--downsampling_scale', default=1, help='The scale for downsampling the image before processing')
@click.option('--post_handle', default=True, type=bool, help='Whether do the post handling part. Default is True')
@click.option('--avoid_duplicate', default=False, type=bool, help='Whether report if already found in last frame')
@click.option('--distance_thresh', default=0.5, type=float, help='Distance threshold of determining if is the same person')
@click.option('--use_camera', default=True, type=bool, help='Use camera as input')
@click.option('--load_suspect', default=True, type=bool, help='Load the suspect data base during initial time, suspect name is the file name')
def main(detection_model, landmarks_model, verbose, poolsize, data_folder, file_ext, scan_rate, mark_face, thread_timeout, downsampling_scale, post_handle, avoid_duplicate, distance_thresh, use_camera, load_suspect):
  if verbose > 0:
    print detection_model, landmarks_model, verbose, poolsize, data_folder, file_ext, scan_rate, mark_face, thread_timeout, downsampling_scale, post_handle, avoid_duplicate, distance_thresh, use_camera, load_suspect

  view.setConfig(verbose)
  pc.setConfig(detection_model, landmarks_model, verbose, poolsize, data_folder, file_ext, scan_rate, mark_face, thread_timeout, downsampling_scale, post_handle, avoid_duplicate, distance_thresh, use_camera, load_suspect)
  pc.setListener(view.getOnUpdate())
  pc.startUp()

  root.protocol("WM_DELETE_WINDOW", on_close)
  root.after(0, updateLoop)
  root.mainloop()
  print 'Exit application'

def SIGINT_handler(signal, frame):
  print '\nuser ctrl+c terminate program...'
  on_close()

if __name__ == '__main__': 
  signal.signal(signal.SIGINT, SIGINT_handler)
  main()