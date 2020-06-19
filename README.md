# musicserver
a private music uploading and streaming service in Django

# stuff that needs to be fixed
- [ ] uploaded media privacy controls
- [ ] write audio -> HLS tool (or improve https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming and submit PR)
- [ ] write orphaned file deletion tool
- [ ] solve potential CSRF in /getkey
- [ ] set enviornment variable "secret" to random valid value
- [ ] add SSL stuff to nginx config