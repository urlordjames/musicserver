# musicserver
a private music uploading and streaming service in Django

# how to deploy

- clone repo
- edit docker-compose.yml
    - configure ```ports``` in ```deployproxy``` to desired value
- add SSL certificates to new directory in project root called ```certs```
- add database with the same name as the ```dbname``` enviornment variable in the ```musicserver``` image to postgres
- edit deployproxy/nginx.conf
    - set ```server_name```
    - set the 301 redirect to the appropriate URL
- run ```docker-compose build```
- set enviornment variable ```secret``` to a new Django secret (I recommend https://djecrety.ir/)
- run ```docker-compose up```