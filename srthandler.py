from watchdog.events import PatternMatchingEventHandler
from webvtt import WebVTT
import os.path
import os

prelog = '[SRT] '
class SrtEventHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=None, ignore_patterns=None, ignore_directories=False, case_sensitive=False, newLogger=None):
        super(SrtEventHandler, self).__init__(['*.srt'], ignore_patterns, ignore_directories, case_sensitive)
        self.logger = newLogger

    def on_created(self, event):
        if not event.is_directory:
            self.logger.debug(prelog + 'creation event: ' + event.src_path)
            vttPath = transcode(event.src_path)
            self.logger.info(prelog + 'transcode done: ' + event.src_path + ' => ' + vttPath)
            os.remove(event.src_path)
            self.logger.info(prelog + 'file removed ' + event.src_path)

def transcode(source):
    sourceDir = os.path.dirname(source)
    sourceFile = os.path.basename(source)
    sourceFileNoExt = os.path.splitext(sourceFile)[0]
    targetFile = sourceFileNoExt + '.vtt'
    convert_ending(source)
    targetFull = sourceDir + '/' + targetFile
    webvtt = WebVTT().from_srt(source)
    webvtt.save(targetFull)
    return targetFull

def convert_ending(source):
    filename = source

    with open(filename, 'r') as f:
        content = f.read()

    with open(filename, 'w') as f:
        f.write(content)

    with open(filename, 'a') as f:
        f.write('\n')
