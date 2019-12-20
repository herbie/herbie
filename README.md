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
