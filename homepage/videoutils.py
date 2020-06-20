import os
from ffprobe import FFProbe
import subprocess
from ffmpeg_streaming import Formats
import ffmpeg_streaming

def getmediainfo(location):
    metadata = FFProbe(location)
    isvideo = False
    assert len(metadata.streams) >= 1
    for stream in metadata.streams:
        if stream.is_video():
            isvideo = True
    if isvideo:
        return "video"
    else:
        return "audio"

def hlsify(title, templocation):
    info = getmediainfo(templocation)
    if info == "video":
        videomedia(title, templocation)
    elif info == "audio":
        audiomedia(title, templocation)
    os.remove(templocation)

def videomedia(title, templocation):
    video = ffmpeg_streaming.input(templocation)
    os.makedirs("deployproxy/media/" + title)
    hls = video.hls(Formats.h264(), hls_time=3)
    os.makedirs("keys/" + title)
    hls.encryption("keys/" + title + "/key", "/getkey/?media=" + title)
    hls.auto_generate_representations()
    hls.output("deployproxy/media/" + title + "/" + "media.m3u8")
    os.remove(templocation)

def audiomedia(title, templocation):
    print(subprocess.check_output(["ffmpeg", "-version"]))
    os.remove(templocation)

def loadkey(medianame):
    f = open(os.path.join("keys", medianame, "key"), "rb")
    key = f.read()
    f.close()
    return key