# Wayne

[![Build Status](https://travis-ci.org/project-a/wayne.svg?branch=master)](https://travis-ci.org/project-a/wayne)

## Setup local environment
In order to set up the local environment quickly, you first need to install [docker](https://docs.docker.com/install/#server) and [docker-compose](https://docs.docker.com/compose/install/).

Afterwards go to the root-folder of the _wayne-project_ and run:
`$ docker-compose up -d`
and then 
`$ docker logs wayne-app -f` 
to watch the progress.

After the boot-process is finished switch to your browser and check: [http://localhost:8000](http://localhost:8000)


_Note:_ Please make sure that port 8000 is not blocked by another service on your host-machine.



## How to generate business object model classes
Model classes can be generated based on the JSON schema definitions by running this command:
`$ python manage.py generatemodels`
