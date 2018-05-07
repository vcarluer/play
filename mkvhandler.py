import logging
from watchdog.events import PatternMatchingEventHandler
from ffmpy import FFmpeg
import os.path
import os
import shutil
from multiprocessing import Process

prelog = '[MKV] '
class MkvEventHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=None, ignore_patterns=None, ignore_directories=False, case_sensitive=False):
        logging.info(prelog + 'Handler ready')
        super(MkvEventHandler, self).__init__(['*.mkv'], ignore_patterns, ignore_directories, case_sensitive)

    def on_created(self, event):
        logging.debug(prelog + 'creation event: ' + event.src_path)
        self.do(event.src_path)

    def on_moved(self, event):
        logging.debug(prelog + 'moved event: ' + event.dst_path)
        self.do(event.dst_path)

    def do(self, path):
        logging.debug(prelog + 'do')
        p = Process(target=self.do_process, args=(path,))
        p.start()
        logging.debug(prelog + 'process started')

    def do_process(self, path):
        logging.info(prelog + 'transcode start ' + path)
        mp4Path = transcode(path)
        logging.info(prelog + 'transcode done: ' + path + ' => ' + mp4Path)
        os.remove(path)
        logging.info(prelog + 'file removed ' + path)

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
