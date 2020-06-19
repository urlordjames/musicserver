# musicserver
a private music uploading and streaming service in Django

# release feature checklist
- [x] user login
- [x] file upload
- [x] ffmpeg optimization of music files (https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming)
- [x] add media player (https://github.com/video-dev/hls.js/)
- [x] add decryption key API
- [x] test deploy web server on local machine and fix resulting bugs
- [ ] write orphaned file deletion tool

# docker image checklist
- [x] disable debug mode
- [x] set db info (dbname, dbuser, dbpass)
- [x] install dependancies
- [ ] set enviornment variable "secret" to random valid value
- [x] configure gunicorn (https://github.com/benoitc/gunicorn)