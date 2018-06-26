import logging
import os.path
import os
import shutil
import time
import glob
from babelfish import Language
from subliminal import download_best_subtitles, region, save_subtitles, scan_video

fileType = 'AVI'
prelog = '[' + fileType + '] '
watchPath = '/var/local/localms'
srtPath = '/var/local/localsrt'
remotePath = '/mnt/ms'
patternPath = watchPath + '/**/*.avi'
logLevel = logging.INFO

def init():
    region.configure('dogpile.cache.dbm', arguments={'filename': 'cachefilesrt.dbm'})

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
    try:
        logging.info(prelog + 'Action start on ' + path)
        logging.debug(prelog + 'getsrt')
        getsrt(path)
        remoteFile = path.replace(watchPath, remotePath)
        remoteDir = os.path.dirname(remoteFile)
        if not os.path.isdir(remoteDir):
            logging.debug(prelog + 'creating remote dir: ' + remoteDir)
            os.makedirs(remoteDir)

        logging.info(prelog + 'copying file to ' + remoteFile)
        shutil.copy(path, remoteFile)
        os.remove(path)
        logging.info(prelog + 'moved file ' + path + ' => ' + remoteFile)
    except:
        logging.exception(prelog)
        if os.path.isfile(path):
            shutil.move(path, path + '.failed')
        pass

# should be done in deficated agent
def getsrt(source):
    try:
        video = scan_video(source)
        videos = [ video ]
        logging.debug(prelog + 'getting subtitles')
        subtitles = download_best_subtitles(videos, {Language('eng'), Language('fra')}, providers=None, provider_configs={'addic7ed': {'username': 'legeek1337', 'password': 'j4TAz0BMsbhBICg7'}, 'opensubtitles': {'username': 'legeek', 'password': 'coolcool'}})
        sourceDir = os.path.dirname(source)
        savePath = sourceDir.replace(watchPath, srtPath)
        if not os.path.isdir(savePath):
            logging.debug(prelog + 'creating srt directory ' + savePath)
            os.makedirs(savePath)
        save_subtitles(video, subtitles[video], directory=savePath)
    except:
        logging.exception(prelog)
        pass

if __name__ == "__main__":
    init()
    init_logging()
    start_watch()
