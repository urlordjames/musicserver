# musicserver
a private music uploading and streaming service in Django

# stuff that needs to be fixed
- [x] uploaded media privacy controls
- [ ] add user-facing config page for media (editable privacy settings)
- [ ] write audio -> HLS tool (or improve https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming and submit PR)
- [x] write orphaned file deletion tool
- [ ] solve potential CSRF in /getkey
- [ ] set enviornment variable "secret" to random valid value
- [ ] add SSL stuff to nginx config