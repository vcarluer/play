from watchdog.events import PatternMatchingEventHandler
from ffmpy import FFmpeg
import os.path
import os
import shutil

prelog = '[MP4] '

class Mp4EventHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=None, ignore_patterns=None, ignore_directories=False, case_sensitive=False, newLogger=None, basePath=None, remoteBasePath=None):
        super(Mp4EventHandler, self).__init__(['*.mp4'], ignore_patterns, ignore_directories, case_sensitive)
        self.logger = newLogger
        self.basePath = basePath
        self.remoteBasePath = remoteBasePath

    def on_created(self, event):
        if not event.is_directory:
            self.logger.debug(prelog + 'creation event: ' + event.src_path)
            remoteFile = event.src_path.replace(self.basePath, self.remoteBasePath)
            remoteDir = os.path.dirname(remoteFile)
            if not os.path.isdir(remoteDir):
                self.logger.debug(prelog + 'creating remote dir: ' + remoteDir)
                os.makedirs(remoteDir)

            shutil.copy(event.src_path, remoteFile)
            os.remove(event.src_path)
            self.logger.debug(prelog + 'moved file ' + event.src_path + ' => ' + remoteFile)