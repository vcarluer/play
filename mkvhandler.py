from watchdog.events import PatternMatchingEventHandler
from ffmpy import FFmpeg
import os.path
import os

prelog = '[MKV] '
class MkvEventHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=None, ignore_patterns=None, ignore_directories=False, case_sensitive=False, newLogger=None):
        super(MkvEventHandler, self).__init__(['*.mkv'], ignore_patterns, ignore_directories, case_sensitive)
        self.logger = newLogger

    def on_created(self, event):
        if not event.is_directory:
            try:
                self.logger.debug(prelog + 'creation event: ' + event.src_path)
                mp4Path = transcode(event.src_path)
                self.logger.info(prelog + 'transcode done: ' + event.src_path + ' => ' + mp4Path)
                os.remove(event.src_path)
                self.logger.info(prelog + 'file removed ' + event.src_path)
            except:
                self.logger.exception(prelog)
                pass

def transcode(source):
    sourceDir = os.path.dirname(source)
    sourceFile = os.path.basename(source)
    sourceFileNoExt = os.path.splitext(sourceFile)[0]
    targetFile = sourceFileNoExt + '.mp4'
    targetFull = sourceDir + '/' + targetFile
    ff=FFmpeg(inputs={source: None}, outputs={targetFull: '-c:a aac -c:v copy -y -loglevel info' })
    # ff.cmd
    ff.run()
    return targetFull
