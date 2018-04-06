from watchdog.observers import Observer
from mkvhandler import MkvEventHandler
from mp4handler import Mp4EventHandler
from srthandler import SrtEventHandler
from vtthandler import VttEventHandler
import logging
import sys
import os
import time

watchPath = '/var/local/localms'
remotePath = '/mnt/ms'

def init_logging():
    logDir = './logs'
    logFile = logDir + '/playwatch.log'
    if not os.path.isdir(logDir):
        os.makedirs(logDir)

    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)

    fileHandler = logging.FileHandler(logFile)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

def watch():
    logging.info('PLAY WATCH READY!!')
    logging.debug('logging system ready')
    mkv_handler = MkvEventHandler()
    mp4_handler = Mp4EventHandler(basePath=watchPath, remoteBasePath=remotePath)
    srt_handler = SrtEventHandler()
    vtt_handler = VttEventHandler(basePath=watchPath, remoteBasePath=remotePath)
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
    logging.info('PLAY WATCH END')

def main():
    init_logging()
    watch()

if __name__ == '__main__':
    main()
