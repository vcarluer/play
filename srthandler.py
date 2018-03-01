import logging
from watchdog.events import PatternMatchingEventHandler
from webvtt import WebVTT
import os.path
import os
import chardet

prelog = '[SRT] '
class SrtEventHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=None, ignore_patterns=None, ignore_directories=False, case_sensitive=False):
        super(SrtEventHandler, self).__init__(['*.srt'], ignore_patterns, ignore_directories, case_sensitive)

    def on_created(self, event):
        if not event.is_directory:
            try:
                logging.debug(prelog + 'creation event: ' + event.src_path)
                vttPath = self.transcode(event.src_path)
                logging.info(prelog + 'transcode done: ' + event.src_path + ' => ' + vttPath)
                os.remove(event.src_path)
                logging.info(prelog + 'file removed ' + event.src_path)
            except:
                logging.exception(prelog)
                pass

    def transcode(self, source):
        sourceDir = os.path.dirname(source)
        sourceFile = os.path.basename(source)
        sourceFileNoExt = os.path.splitext(sourceFile)[0]
        targetFile = sourceFileNoExt + '.vtt'
        self.convert_ending(source)
        targetFull = sourceDir + '/' + targetFile
        webvtt = WebVTT().from_srt(source)
        webvtt.save(targetFull)
        return targetFull

    def convert_ending(self, source):
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
