from watchdog.observers import Observer
from mkvhandler import MkvEventHandler
from mp4handler import Mp4EventHandler
import logging
import sys
import os
import time

logger = None
watchPath = '/var/local/localms'
remotePath = '/mnt/ms'

def init_logger():
    logging.basicConfig(level=logging.INFO)
    global logger
    logger = logging.getLogger('watcher')
    logger.setLevel(logging.DEBUG)
    logDir = './logs'
    logFile = logDir + '/playwatch.log'
    if not os.path.isdir(logDir):
        os.makedirs(logDir)

    logger.addHandler(logging.FileHandler(logFile))
    logger.addHandler(logging.StreamHandler(sys.stdout))

def watch():
    logger.debug('logging system ready')
    mkv_handler = MkvEventHandler(newLogger=logger)
    mp4_handler = Mp4EventHandler(newLogger=logger, basePath=watchPath, remoteBasePath=remotePath)
    observer = Observer()
    observer.schedule(mkv_handler, watchPath, recursive=True)
    observer.schedule(mp4_handler, watchPath, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    init_logger()
    watch()

if __name__ == '__main__':
    main()
