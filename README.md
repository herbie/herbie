# Wayne

[![Build Status](https://travis-ci.org/project-a/wayne.svg?branch=master)](https://travis-ci.org/project-a/wayne)

## Quickstart

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
