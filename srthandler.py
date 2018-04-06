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
        logging.info(prelog + 'Handler ready')

    def on_created(self, event):
        logging.debug(prelog + 'creation event: ' + event.src_path)
        self.do(event.src_path)

    def on_moved(self, event):
        logging.debug(prelog + 'moved event: ' + event.dst_path)
        self.do(event.dst_path)

    def do(self, path):
        try:
            logging.info(prelog + 'transcoding: ' + path)
            vttPath = self.transcode(path)
            logging.info(prelog + 'transcode done: ' + path + ' => ' + vttPath)
            os.remove(path)
            logging.info(prelog + 'file removed ' + path)
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
