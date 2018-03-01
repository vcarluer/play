import logging
from watchdog.events import PatternMatchingEventHandler
import os.path
import os
import shutil
from babelfish import Language
from subliminal import download_best_subtitles, region, save_subtitles, scan_video

prelog = '[MP4] '

class Mp4EventHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=None, ignore_patterns=None, ignore_directories=False, case_sensitive=False, basePath=None, remoteBasePath=None):
        super(Mp4EventHandler, self).__init__(['*.mp4'], ignore_patterns, ignore_directories, case_sensitive)
        self.basePath = basePath
        self.remoteBasePath = remoteBasePath

    def on_created(self, event):
        self.do(event.src_path)

    def on_moved(self, event):
        self.do(event.dst_path)

    def do(self, path):
        try:
            logging.debug(prelog + 'creation event: ' + path)
            logging.debug(prelog + 'getsrt')
            self.getsrt(path)
            remoteFile = path.replace(self.basePath, self.remoteBasePath)
            remoteDir = os.path.dirname(remoteFile)
            if not os.path.isdir(remoteDir):
                logging.debug(prelog + 'creating remote dir: ' + remoteDir)
                os.makedirs(remoteDir)

            logging.debug(prelog + 'copying file to ' + remoteFile)
            shutil.copy(path, remoteFile)
            os.remove(path)
            logging.debug(prelog + 'moved file ' + path + ' => ' + remoteFile)
        except:
            logging.exception(prelog)
            pass

    def getsrt(self, source):
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
