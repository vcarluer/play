import logging
from watchdog.events import PatternMatchingEventHandler
import os.path
import os
import shutil

prelog = '[VTT] '

class VttEventHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=None, ignore_patterns=None, ignore_directories=False, case_sensitive=False, basePath=None, remoteBasePath=None):
        super(VttEventHandler, self).__init__(['*.vtt'], ignore_patterns, ignore_directories, case_sensitive)
        logging.info(prelog + 'Handler ready')
        self.basePath = basePath
        self.remoteBasePath = remoteBasePath

    def on_created(self, event):
        logging.debug(prelog + 'creation event: ' + event.src_path)
        self.do(event.src_path)

    def on_moved(self, event):
        logging.debug(prelog + 'moved event: ' + event.dst_path)
        self.do(event.dst_path)

    def do(self, path):
        try:
            logging.debug(prelog + 'Action start on ' + path)
            remoteFile = path.replace(self.basePath, self.remoteBasePath)
            remoteDir = os.path.dirname(remoteFile)
            if not os.path.isdir(remoteDir):
                logging.debug(prelog + 'creating remote dir: ' + remoteDir)
                os.makedirs(remoteDir)

            shutil.copy(path, remoteFile)
            os.remove(path)
            logging.info(prelog + 'moved file ' + path + ' => ' + remoteFile)
        except:
            logging.exception(prelog)
            pass
