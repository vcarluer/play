import logging
import os.path
import os
import shutil
import time
import glob
from babelfish import Language
from subliminal import download_best_subtitles, region, save_subtitles, scan_video

fileType = 'MP4'
prelog = '[' + fileType + '] '
watchPath = '/var/local/localms'
remotePath = '/mnt/ms'
patternPath = watchPath + '/**/*.mp4'
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

def getsrt(source):
    try:
        region.configure('dogpile.cache.dbm', arguments={'filename': '/var/local/localms/cachefilesrt.dbm'})
        video = scan_video(source)
        videos = [ video ]
        logging.debug(prelog + 'getting subtitles')
        subtitles = download_best_subtitles(videos, {Language('eng'), Language('fra')}, providers=None, provider_configs={'addic7ed': {'username': 'legeek1337', 'password': 'j4TAz0BMsbhBICg7'}, 'opensubtitles': {'username': 'legeek', 'password': 'coolcool'}})
        save_subtitles(video, subtitles[video])
    except:
        logging.exception(prelog)
        pass

if __name__ == "__main__":
    init_logging()
    start_watch()
