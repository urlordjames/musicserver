import os
from ffmpeg_streaming import Formats
import ffmpeg_streaming

def hlsify(title, templocation):
    video = ffmpeg_streaming.input(templocation)
    os.makedirs("deployproxy/media/" + title)
    hls = video.hls(Formats.h264(), hls_time=3)
    os.makedirs("keys/" + title)
    hls.encryption("keys/" + title + "/key", "/getkey/?media=" + title)
    hls.auto_generate_representations()
    hls.output("deployproxy/media/" + title + "/" + "media.m3u8")
    os.remove(templocation)

def loadkey(medianame):
    f = open(os.path.join("keys", medianame, "key"), "rb")
    key = f.read()
    f.close()
    return key