import logging
import os.path
import os
import time
import glob
from webvtt import WebVTT
import chardet

fileType = 'SRT'
prelog = '[' + fileType + '] '
watchPath = '/var/local/localms'
patternPath = watchPath + '/**/*.srt'
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
    logging.info(prelog + 'transcoding: ' + path)
    vttPath = transcode(path)
    logging.info(prelog + 'transcode done: ' + path + ' => ' + vttPath)
    os.remove(path)
    logging.info(prelog + 'file removed ' + path)

def transcode(source):
    sourceDir = os.path.dirname(source)
    sourceFile = os.path.basename(source)
    sourceFileNoExt = os.path.splitext(sourceFile)[0]
    targetFile = sourceFileNoExt + '.vtt'
    convert_ending(source)
    clean_file(source)
    targetFull = sourceDir + '/' + targetFile
    logging.debug(prelog + 'targetFull: ' + targetFull)
    webvtt = WebVTT().from_srt(source)
    webvtt.save(targetFull)
    return targetFull

def clean_file(filename):
    logging.debug(prelog + 'clean file')
    # function to check if the line can be deleted
    def is_all_whitespace(line):
        for char in line:
            if char != ' ' and char != '\n' and char != '\t':
                logging.debug(prelog + 'Not an empty line')
                return False
        logging.debug(prelog + 'empty line detected')
        return True

    # generates the new lines
    with open(filename, 'r') as file:
        file_out = []
        for line in file:
            if is_all_whitespace(line):
                line = '\n'
            file_out.append(line)

    # removes whitespaces at the end of file
    while file_out[-1] == '\n':  # while the last item in lst is blank
        file_out.pop(-1)  # removes last element
        logging.debug(prelog + 'poping line')

    # writes the new the output to file
    with open(filename, 'w') as file:
        logging.debug(prelog + 'writing new file')
        file.write(''.join(file_out))

def convert_ending(source):
    logging.debug(prelog + 'concert ending ' + source)
    filename = source

    with open(filename, mode='rb') as f:
        readSrt = f.read()

    encoding = chardet.detect(readSrt)['encoding']
    if encoding:
        logging.debug(prelog + 'detected encoding: ' + encoding)
        content = readSrt.decode(encoding).encode('utf8')
    else:
        content = readSrt

    with open(filename, mode='wb') as f:
        f.write(content)

    with open(filename, encoding='utf-8', mode='a') as f:
        f.write('\n')

if __name__ == "__main__":
    init_logging()
    start_watch()