from watchdog.events import PatternMatchingEventHandler
import os.path
import os
import shutil
from babelfish import Language
from subliminal import download_best_subtitles, region, save_subtitles, scan_video

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
            self.logger.debug(prelog + 'getsrt')
            self.getsrt(event.src_path)
            remoteFile = event.src_path.replace(self.basePath, self.remoteBasePath)
            remoteDir = os.path.dirname(remoteFile)
            if not os.path.isdir(remoteDir):
                self.logger.debug(prelog + 'creating remote dir: ' + remoteDir)
                os.makedirs(remoteDir)

            shutil.copy(event.src_path, remoteFile)
            os.remove(event.src_path)
            self.logger.debug(prelog + 'moved file ' + event.src_path + ' => ' + remoteFile)

    def getsrt(self, source):
        region.configure('dogpile.cache.dbm', arguments={'filename': 'cachefilesrt.dbm'})
        video = scan_video(source)
        videos = [ video ]
        self.logger.debug(prelog + 'getting subtitles')
        subtitles = download_best_subtitles(videos, {Language('eng'), Language('fra')}, providers=None, provider_configs={'addic7ed': {'username': 'legeek1337', 'password': 'j4TAz0BMsbhBICg7'}, 'opensubtitles': {'username': 'legeek', 'password': 'coolcool'}})
        save_subtitles(video, subtitles[video])
