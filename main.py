import signal
import sys
import time
import getopt

from controller import Controller
pc = Controller()

isActive = True

def main(argv):
  # handle options
  # def usage():
  #   print 'usage: %s ' % argv[0]
  #   return 100
  # try:
  #   (opt, args) = getopt.getopt(argv[1:], '')
  # except getopt.GetoptError:
  #   return usage()
  # if not args: 
  #   return usage()

  pc.startUp()

  # busy loop to hold the main thread not exit
  while isActive:
    # TODO: monitor the health of the thread pool
    pc.logInfo()
    time.sleep(3)
    pass

def SIGINT_handler(signal, frame):
  print '\nuser ctrl+c terminate program...'
  pc.cleanUp()
  isActive = False
  sys.exit(0)

if __name__ == '__main__': 
  signal.signal(signal.SIGINT, SIGINT_handler)
  sys.exit(main(sys.argv))