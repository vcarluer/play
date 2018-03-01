import os.path
from ffmpy import FFmpeg

def transcode(source):
    sourceDir = os.path.dirname(source)
    sourceFile = os.path.basename(source)
    sourceFileNoExt = os.path.splitext(sourceFile)[0]
    targetFile = sourceFileNoExt + '.mp4'
    targetFull = sourceDir + '/' + targetFile
    ff=FFmpeg(inputs={source: None}, outputs={targetFull: '-c:a aac -c:v copy -y -loglevel error' })
    # ff.cmd
    ff.run()
    return targetFull

def transcode_agent(queue, playQueue):
    print('Transcode agent starting')
    doLoop = True
    while doLoop:
        if not queue.empty():
            source = queue.get()
            if source == 'exit':
                print('Transcode agent exit')
                doLoop = False
            else:
                print('Transcode agent transcode ' + source)
                target = transcode(source)
                playQueue.put('transcoded:' + target)
