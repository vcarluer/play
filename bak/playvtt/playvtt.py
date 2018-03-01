from webvtt import WebVTT

# Need to convert to unix + utf8 before
webvtt = WebVTT().from_srt('/home/dl/to_vtt/Thor/Thor.srt')
webvtt.save('/home/dl/vtt/Thor/Thor.vtt')
