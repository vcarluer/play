import logging
import os.path
import os
import shutil
import time
import glob

fileType = 'VTT'
prelog = '[' + fileType + '] '
watchPath = '/var/local/localms'
remotePath = '/mnt/ms'
patternPath = watchPath + '/**/*.vtt'
logLevel = logging.DEBUG

def init_logging():
    logDir = './logs'
    logFile = logDir + '/' + fileType + 'parser.log'
    if not os.path.isdir(logDir):
        os.makedirs(logDir)

    logging.basicConfig(filename=logFile,level=logLevel)
    logging.debug(("{}Logger ready").format(prelog))

def start_watch():
    while True:
        logging.debug(("{}loop").format(prelog))
        for fileName in glob.glob(patternPath, recursive=True):
            logging.debug(("{}{} file detected in {}: {}").format(prelog, fileType, watchPath, fileName))
            handle_file(fileName)

        logging.debug(("{} waiting").format(prelog))
        time.sleep(10)

def handle_file(path):
    logging.debug(prelog + 'Action start on ' + path)
    remoteFile = path.replace(watchPath, remotePath)
    remoteDir = os.path.dirname(remoteFile)
    if not os.path.isdir(remoteDir):
        logging.debug(prelog + 'creating remote dir: ' + remoteDir)
        os.makedirs(remoteDir)

    shutil.copy(path, remoteFile)
    os.remove(path)
    logging.info(prelog + 'moved file ' + path + ' => ' + remoteFile)

if __name__ == "__main__":
    init_logging()
    start_watch()
