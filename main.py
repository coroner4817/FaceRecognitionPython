import signal
import sys
import time
import getopt
import click

from controller import Controller
pc = Controller()
isActive = True

@click.command()
@click.option('--detection_model', default="hog", help='Available models: "hog", "cnn", "cnn" is more accurate but slow and might yield error')
@click.option('--landmarks_model', default="small", help='Available models: "small", "large", "large" is using 68 landmarks points')
@click.option('--verbose', default=1, help='verbose level 0-2')
@click.option('--poolsize', default=4, help='ThreadPool size base on CPU number. Recommand 4')
@click.option('--data_folder', default='./captures/', help='Data folder for searching for input files')
@click.option('--file_ext', default='.JPG', help='Image file extension of the camera output')
@click.option('--scan_rate', default=1, help='How long to sleep before next file scan, should match camera dump rate')
@click.option('--mark_face', default=False, type=bool, help='If set to True will draw a bounding box on the output image')
@click.option('--thread_timeout', default=0, help='Set the timeout for processing time of thread pool. If set to 0 then is not monitored')
@click.option('--downsampling_scale', default=1, help='The scale for downsampling the image before processing')
def main(detection_model, landmarks_model, verbose, poolsize, data_folder, file_ext, scan_rate, mark_face, thread_timeout, downsampling_scale):
  if verbose > 0:
    print detection_model, landmarks_model, verbose, poolsize, data_folder, file_ext, scan_rate, mark_face, thread_timeout, downsampling_scale
  pc.setConfig(detection_model, landmarks_model, verbose, poolsize, data_folder, file_ext, scan_rate, mark_face, thread_timeout, downsampling_scale)
  pc.startUp()

  # busy loop to hold the main thread not exit
  while isActive:
    # TODO: monitor the health of the thread pool
    if verbose > 0:
      pc.logInfo()
      time.sleep(3)

def SIGINT_handler(signal, frame):
  print '\nuser ctrl+c terminate program...'
  pc.cleanUp()
  isActive = False
  sys.exit(0)

if __name__ == '__main__': 
  signal.signal(signal.SIGINT, SIGINT_handler)
  main()