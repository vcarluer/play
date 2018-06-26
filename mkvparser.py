import logging
from ffmpy import FFmpeg
import os.path
import os
import shutil
import time
import glob

prelog = '[MKV] '
watchPath = '/var/local/localms'
searchPattern = '/**/*.mkv'
logLevel = logging.INFO
logFileName = 'mkvparser.log'

def init_logging(fileName):
    logDir = './logs'
    logFile = logDir + '/' + fileName
    if not os.path.isdir(logDir):
        os.makedirs(logDir)

    logging.basicConfig(filename=logFile,level=logLevel)
    logging.debug(("{}Logger ready").format(prelog))

def convert_all(convertPath, logFile):

    init_logging(logFile)
    logging.debug(("{}convert_all").format(prelog))

    loop_files(convertPath)

def loop_files(loopPath):
    patternPath = loopPath + searchPattern
    print(patternPath)
    for fileName in glob.glob(patternPath, recursive=True):
        print(fileName)
        logging.debug(("{}MKV file detected in {}: {}").format(prelog, loopPath, fileName))
        handle_file(fileName)

def start_watch(loopPath):
    while True:
        logging.debug(("{}loop").format(prelog))
        loop_files(loopPath)
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
        ext = '.mp4'
        if 'VP9' in source:
            ext = '.webm'
        targetFile = sourceFileNoExt + ext
        tempFull = '/tmp/' + targetFile
        logging.debug(prelog + 'tempFull: ' + tempFull)
        targetFull = sourceDir + '/' + targetFile
        targetTranscode = tempFull
        isMnt = False
        # direct transcode if from mnt storage box
        if 'mnt/.sb' in source:
            targetTranscode = targetFull
            isMnt = True
            
        logging.debug(prelog + 'targetFull: ' + targetFull)
        if ext == '.webm':
            logging.info('VP9 detected. Audio to libvorbis and webm container')
            ff=FFmpeg(inputs={source: None}, outputs={targetTranscode: '-c:a libvorbis -c:v copy -y -loglevel info' })
        else:
            logging.debug('Assume video is h264. Audio to aac and mp4 container')
            ff=FFmpeg(inputs={source: None}, outputs={targetTranscode: '-c:a aac -c:v copy -y -loglevel info' })
        # ff.cmd
        ff.run()
        if isMnt == False:
            shutil.move(tempFull, targetFull)

        return targetFull
    except:
        logging.exception(prelog)
        if os.path.isfile(source):
            shutil.move(source, source + '.failed')
        pass
    return None

if __name__ == "__main__":
    init_logging(logFileName)
    start_watch(watchPath)
