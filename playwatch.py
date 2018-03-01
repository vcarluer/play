from watchdog.observers import Observer
from mkvhandler import MkvEventHandler
import logging
import sys
import os
import time

logger = None
watchPath = '/var/local/localms'

def init_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('watcher')
    logger.setLevel(logging.DEBUG)
    logDir = './logs'
    logFile = logDir + '/playwatch.log'
    if not os.path.isdir(logDir):
        os.makedirs(logDir)

    logger.addHandler(logging.FileHandler(logFile))
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.debug('logging system ready')
    event_handler = MkvEventHandler(newLogger=logger)
    observer = Observer()
    observer.schedule(event_handler, watchPath, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    init_logger()

if __name__ == '__main__':
    main()
