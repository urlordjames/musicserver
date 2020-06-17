# musicserver
a private music uploading and streaming service in Django

# release feature checklist
- [x] user login
- [x] file upload
- [x] ffmpeg optimization of music files (https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming)
- [x] add media player (https://github.com/video-dev/hls.js/)
- [x] add decryption key API
- [ ] test deletetion of orphaned files (https://github.com/ledil/django-orphaned)
- [ ] test deploy web server on local machine and fix resulting bugs

# docker image checklist
- [ ] disable debug mode
- [ ] set db info (dbname, dbuser, dbpass)
- [ ] install dependancies
- [ ] set enviornment variable "secret" to random valid value
- [ ] configure gunicorn (https://github.com/benoitc/gunicorn)