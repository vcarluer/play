from webvtt import WebVTT

webvtt = WebVTT().from_srt('/home/dl/to_vtt/Thor/Thor.srt')
webvtt.save('/home/dl/vtt/Thor/Thor.vtt')
