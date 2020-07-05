# musicserver
a private music uploading and streaming service in Django

# how to deploy

- clone repo
- edit docker-compose.yml
    - set the enviornment variable ```secret``` in ```musicserver``` to a new value
    - configure ```ports``` in ```deployproxy``` to desired value
- add SSL certificates to new directory in project root called ```certs```
- add database with the same name as the ```dbname``` enviornment variable in the ```musicserver``` image to postgres
- run ```docker-compose up```