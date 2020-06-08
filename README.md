# musicserver
a private music uploading and streaming service in Django

# release feature checklist
- [x] user login
- [x] file upload
- [ ] ffmpeg optimization of music files (https://github.com/kkroening/ffmpeg-python)
    - [ ] maybe use HLS or DASH (???)
- [ ] test deletetion of orphaned files (https://github.com/ledil/django-orphaned)
- [ ] test deploy web server on local machine and fix resulting bugs

# deploy checklist
- [ ] create circleci script which does the following
    - [ ] installs dependancies (https://github.com/ledil/django-orphaned, https://github.com/kkroening/ffmpeg-python)
    - [ ] sets the enviornment variable "secret" to a new securely random valid Django secret key
    - [ ] sets up production HTTP server (most likely https://github.com/benoitc/gunicorn)
    - [ ] sets up a cron job to automatically clear orphaned files (https://github.com/ledil/django-orphaned)
- [ ] give out accounts to friends and test appropriate file size limits