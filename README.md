# Wayne

[![Build Status](https://travis-ci.org/project-a/wayne.svg?branch=master)](https://travis-ci.org/project-a/wayne)


## Overview

Two Problems that can often be observed in a distributed service architecture are:

A. **Too many dependencies** between services.

B. No common **platform-wide definition** of a data object or business entity.

Wayne approaches those problems with the idea of a _schema registry combined with a central data store_ for business 
entities. 
It is built with Django and comes with a simple API to create business entities. The integration of _json-schema_ 
allows to define custom schema definitions, that will be used to validate the entities. A service that
needs updates of a certain entity-type is also able to subscribe to _event-streams_, the default technology 
for that is Kafka.

The philosophy behind Wayne is to avoid behavior that appears to a developers as "magic" and instead is built in very
straightforward way, following Django best practices. It is also meant to be extendable and easy to adapt.

**Further reading:**

- [Core Concepts of Wayne](docs/core_concepts.md)


## Quickstart

In order to set up the local environment quickly, you first need to install [docker](https://docs.docker.com/install/#server)
and [docker-compose](https://docs.docker.com/compose/install/).

Afterwards go to the root-folder of the _wayne-project_ and run:
`$ docker-compose up -d`
and then 
`$ docker logs wayne-app -f` 
to watch the progress.

After the boot-process is finished switch to your browser and check: [http://localhost:8000](http://localhost:8000)


_Note:_ Please make sure that port 8000 is not blocked by another service on your host-machine.

# How to setup wayne for your project?
### 1 Clone/Fork
In order to setup a Wayne-Project from scratch you can either fork or clone the repository. We suggest you to fork the project, 
because like that you have a separate repository so you can make custom modifications (e.g. change the messaging provider) 
and at the same time receive changes from the official repository in an easy manner

### 2 Add Business Entities Schemas Package
Next step is to define your schemas for your business entities and integrate them with Wayne. There are 2 choices, having a different
repository for your schemas and load them to wayne as a python package with pip, or adding them directly to the Wayne as a python package

##### Business Entities Schemas package folders structure
```
---business_entities_schemas
        init.py 
        ------  business_entity1
                    ------- business_entity1_v1.json
                    ------- business_entity1_v2.json    
        ------  business_entity2
```
##### example
```
---wayne-json-schema
        init.py
        ------  customer
                    ------- customer_v1.json
                    ------- customer_v2.json    
        ------  product
                    ------- product_v1.json
```
https://github.com/project-a/wayne-json-schema


##### Different Github Repository
- Create a github repository
- In requirements.txt file append your schemas repository url in order for pip to collect your package.
(e.g.  git+https://github.com/project-a/wayne-json-schema.git)
- In setting.py file of Wayne project assign your package name to the 'SCHEMA_REGISTRY_PACKAGE' variable

(Keep in mind that in case of a private repository, it also needs to provide a private ssh key to the docker container and pull the project with ssh in order for Wayne
to have access on the repository. For the developing process you can directly provide you personal private ssh key but for production you need to create a new one
for Wayne)

##### Add them directly to the Project
- Add/Create your package to the root folder of Wayne Project.
- In setting.py file of Wayne project assign your package name to the 'SCHEMA_REGISTRY_PACKAGE' variable

# Run Wayne on Docker
- Clone the project(from your forked or the official repository)
- Build and run Wayne
```
docker-compose up -d --build
```
- Connect to wayne-app container
```
docker exec -it wayne-app bash
```
- Generate business object model classes from your schemas package
```
python manage.py generatemodels
```

- Create and execute migration files to initialize your database
```
python manage.py makemigrations
python manage.py migrate
```

## How to generate business object model classes
Model classes can be generated based on the JSON schema definitions by running this command:
`$ python manage.py generatemodels`


## Import business json schemas

Run the command to import json schemas into db

`python manage.py import_json_schemas`


## API Authentication
- [How to add an Auth Token for a Service?](docs/add_service_client.md)

## Admin Panel
- [How to add social login?](docs/social_login.md)

## How to change the messaging system?
The default Wayne setup uses Kafka (mainly because it's very popular) for distributing
the business entity messages in a JSON format. But it should be easy to use any other
messaging system:

The messaging is implemented in
[wayneapp/services/message_publisher.py](wayneapp/services/message_publisher.py).
To replace the Kafka client with any other client, you just have to change the
implementation of the internal `_send_message` method of the `MessagePublisher` class.

Then you can also remove or replace the Kafka connection settings in
[wayne/settings.py](wayne/settings.py), and also remove or replace the Kafka and
Zookeeper images in the [docker-compose.yml](docker-compose.yml).


## Wayne - Development
- [PyCharm Configuration](docs/pycharm_config.md)
