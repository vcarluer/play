import logging
from watchdog.events import PatternMatchingEventHandler
import os.path
import os
import shutil

prelog = '[VTT] '

class VttEventHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=None, ignore_patterns=None, ignore_directories=False, case_sensitive=False, basePath=None, remoteBasePath=None):
        super(VttEventHandler, self).__init__(['*.vtt'], ignore_patterns, ignore_directories, case_sensitive)
        self.basePath = basePath
        self.remoteBasePath = remoteBasePath

    def on_created(self, event):
        if not event.is_directory:
            try:
                logging.debug(prelog + 'creation event: ' + event.src_path)
                remoteFile = event.src_path.replace(self.basePath, self.remoteBasePath)
                remoteDir = os.path.dirname(remoteFile)
                if not os.path.isdir(remoteDir):
                    logging.debug(prelog + 'creating remote dir: ' + remoteDir)
                    os.makedirs(remoteDir)

                shutil.copy(event.src_path, remoteFile)
                os.remove(event.src_path)
                logging.debug(prelog + 'moved file ' + event.src_path + ' => ' + remoteFile)
            except:
                logging.exception(prelog)
                pass
