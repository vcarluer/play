import logging
from watchdog.events import PatternMatchingEventHandler
from ffmpy import FFmpeg
import os.path
import os
import shutil

prelog = '[MKV] '
class MkvEventHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=None, ignore_patterns=None, ignore_directories=False, case_sensitive=False):
        super(MkvEventHandler, self).__init__(['*.mkv'], ignore_patterns, ignore_directories, case_sensitive)

    def on_created(self, event):
        self.do(event.src_path)

    def on_moved(self, event):
        self.do(event.dst_path)

    def do(self, path):
        try:
            logging.debug(prelog + 'creation event: ' + path)
            mp4Path = transcode(path)
            logging.info(prelog + 'transcode done: ' + path + ' => ' + mp4Path)
            os.remove(path)
            logging.info(prelog + 'file removed ' + path)
        except:
            logging.exception(prelog)
            pass

def transcode(source):
    sourceDir = os.path.dirname(source)
    sourceFile = os.path.basename(source)
    sourceFileNoExt = os.path.splitext(sourceFile)[0]
    targetFile = sourceFileNoExt + '.mp4'
    tempFull = '/tmp/' + targetFile
    targetFull = sourceDir + '/' + targetFile
    ff=FFmpeg(inputs={source: None}, outputs={tempFull: '-c:a aac -c:v copy -y -loglevel info' })
    # ff.cmd
    ff.run()
    shutil.move(tempFull, targetFull)
    return targetFull
