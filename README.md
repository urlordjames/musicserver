# musicserver
a private music uploading and streaming service in Django

# stuff that needs to be fixed
- [x] uploaded media privacy controls
- [ ] add user-facing config page for media (editable privacy settings)
- [ ] write audio -> HLS tool (https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming can't be used for audio since it was built for video and I would pretty much just have to rewrite the entire thing)
- [x] write orphaned file deletion tool
- [ ] solve potential CSRF in /getkey
- [ ] set enviornment variable "secret" to random valid value
- [ ] add SSL stuff to nginx config