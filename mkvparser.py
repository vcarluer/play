import logging
from ffmpy import FFmpeg
import os.path
import os
import shutil
import time
import glob

prelog = '[MKV] '
watchPath = '/var/local/localms'
patternPath = watchPath + '/**/*.mkv'
logLevel = logging.DEBUG

def init_logging():
    logDir = './logs'
    logFile = logDir + '/mkvparser.log'
    if not os.path.isdir(logDir):
        os.makedirs(logDir)

    logging.basicConfig(filename=logFile,level=logLevel)
    logging.debug(("{}Logger ready").format(prelog))

def start_watch():
    while True:
        logging.debug(("{}loop").format(prelog))
        for fileName in glob.glob(patternPath, recursive=True):
            logging.debug(("{}MKV file detected in {}: {}").format(prelog, watchPath, fileName))
            handle_file(fileName)

        logging.debug(("{} waiting").format(prelog))
        time.sleep(10)

def handle_file(path):
    try:
        logging.info(prelog + 'transcode start ' + path)
        mp4Path = transcode(path)
        logging.info(prelog + 'transcode done: ' + path + ' => ' + mp4Path)
        os.remove(path)
        logging.info(prelog + 'file removed ' + path)
    except:
        logging.exception(prelog)
        if os.path.isfile(path):
            shutil.move(path, path + '.failed')
        pass

def transcode(source):
    try:
        sourceDir = os.path.dirname(source)
        sourceFile = os.path.basename(source)
        sourceFileNoExt = os.path.splitext(sourceFile)[0]
        targetFile = sourceFileNoExt + '.mp4'
        tempFull = '/tmp/' + targetFile
        logging.debug(prelog + 'tempFull: ' + tempFull)
        targetFull = sourceDir + '/' + targetFile
        logging.debug(prelog + 'targetFull: ' + targetFull)
        ff=FFmpeg(inputs={source: None}, outputs={tempFull: '-c:a aac -c:v copy -y -loglevel info' })
        # ff.cmd
        ff.run()
        shutil.move(tempFull, targetFull)
        return targetFull
    except:
        logging.exception(prelog)
        if os.path.isfile(source):
            shutil.move(source, source + '.failed')
        pass
    return None

if __name__ == "__main__":
    init_logging()
    start_watch()
