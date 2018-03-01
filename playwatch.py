from watchdog.observers import Observer
from mkvhandler import MkvEventHandler
from mp4handler import Mp4EventHandler
from srthandler import SrtEventHandler
from vtthandler import VttEventHandler
import logging
import sys
import os
import time

logger = None
watchPath = '/var/local/localms'
remotePath = '/mnt/ms'

def init_logger():
    logging.basicConfig(level=logging.ERROR)
    global logger
    logger = logging.getLogger('watcher')
    logger.setLevel(logging.DEBUG)
    logDir = './logs'
    logFile = logDir + '/playwatch.log'
    if not os.path.isdir(logDir):
        os.makedirs(logDir)

    logger.addHandler(logging.FileHandler(logFile))

def watch():
    logger.info('PLAY WATCH READY!!')
    logger.debug('logging system ready')
    mkv_handler = MkvEventHandler(newLogger=logger)
    mp4_handler = Mp4EventHandler(newLogger=logger, basePath=watchPath, remoteBasePath=remotePath)
    srt_handler = SrtEventHandler(newLogger=logger)
    vtt_handler = VttEventHandler(newLogger=logger, basePath=watchPath, remoteBasePath=remotePath)
    observer = Observer()
    observer.schedule(mkv_handler, watchPath, recursive=True)
    observer.schedule(mp4_handler, watchPath, recursive=True)
    observer.schedule(srt_handler, watchPath, recursive=True)
    observer.schedule(vtt_handler, watchPath, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    logger.info('PLAY WATCH END')

def main():
    init_logger()
    watch()

if __name__ == '__main__':
    main()
