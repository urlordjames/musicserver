import os
import subprocess
import secrets
from ffprobe import FFProbe
from ffmpeg_streaming import Formats
import ffmpeg_streaming

def getmediainfo(location):
    metadata = FFProbe(location)
    isvideo = False
    if len(metadata.streams) < 1:
        return None
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
    else:
        os.remove(templocation)

def videomedia(title, templocation):
    video = ffmpeg_streaming.input(templocation)
    os.makedirs(os.path.join("deployproxy", "media", title))
    hls = video.hls(Formats.h264(), hls_time=3)
    os.makedirs("keys/" + title)
    hls.encryption(os.path.join("keys", title, "key"), "/getkey/?media=" + title)
    hls.auto_generate_representations()
    hls.output(os.path.join("deployproxy", "media", title, "media.m3u8"))
    os.remove(templocation)

def audiomedia(title, templocation):
    os.makedirs(os.path.join("deployproxy", "media", title))
    keyuri = "/getkey/?media=" + title
    os.makedirs(os.path.join("keys", title))
    keypath = os.path.join("keys", title, "key")
    with open(keypath, "wb") as f:
        f.write(secrets.token_bytes(16))
    IV = secrets.token_hex(16)
    tempinfo = os.path.join("temp", title + ".keyinfo")
    with open(tempinfo, "w") as f:
        f.writelines([keyuri + "\n", keypath + "\n", IV])
    subprocess.run(["ffmpeg", "-i", templocation, "-f", "hls", "-hls_time", "3", "-hls_playlist_type", "event", "-hls_key_info_file", tempinfo, os.path.join("deployproxy", "media", title, "media.m3u8")])
    os.remove(templocation)
    os.remove(tempinfo)

def loadkey(medianame):
    with open(os.path.join("keys", medianame, "key"), "rb") as f:
        key = f.read()
    return key