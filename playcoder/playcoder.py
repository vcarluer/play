from ffmpy import FFmpeg

ff=FFmpeg(inputs={'/home/dl/to_transcode/Thor/Thor.mkv': None}, outputs={'/home/dl/transcoded/Thor/Thor.mp4': '-c:a aac -c:v copy' })
ff.cmd
ff.run()
