import os.path
from ffmpy import FFmpeg

class Transcoder:
    def transcode(self, source):
        sourceDir = os.path.dirname(source)
        sourceFile = os.path.basename(source)
        sourceFileNoExt = os.path.splitext(sourceFile)[0]
        targetFile = sourceFileNoExt + '.mp4'
        targetFull = sourceDir + '/' + targetFile
        ff=FFmpeg(inputs={source: None}, outputs={targetFull: '-c:a aac -c:v copy' })
        ff.cmd
        ff.run()

tc = Transcoder()
tc.transcode('/var/local/localms/movies/Sample (2017)/sample.mkv')
