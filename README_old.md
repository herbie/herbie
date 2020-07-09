


1. After cloning this repository, navigate to the root folder and run one of the following commands:
    * To start with Kafka: `docker-compose -f docker-compose-kafka.yml up -d`
    * To star with Google Pub/Sub: `docker-compose -f docker-compose-google-pubsub.yml up -d`
    
   On first run, Docker builds the required images and installs the dependencies listed in [`requirements.txt`](./requirements.txt).


1. Run `$ docker logs herbie-app -f` to start the app and watch the progress.
1. After the app has booted, connect to herbie-app container:

    ```
    docker exec -it herbie-app bash
    ```    

1. In your browser, open the admin dashboard at [http://localhost:8000/admin](http://localhost:8000/admin).

    > **_NOTE:_** Make sure that port 8000 isn't blocked by another service on your host machine.

1. Enter the credentials for the admin user that you created in step 5.3 and log in.




# How to set up your own Herbie project

## 1. Either fork or clone this repository

We suggest you to fork the project, 
because you'll be able to make custom modifications (e.g. change the messaging provider) but you'll also get changes from the official repository.

## 2. Define your business entities and integrate them with Herbie
    
You define your business entities with JSON schemas. There are two ways to define your business entities:

1. Create a separate repository for your schemas and use pip to load them into Herbie as a Python package.

1. Store your schemas in a Python package that lives directly in your Herbie repository.


### Package structure

Regardless of your preferred option, you should structure your package according to the following template:

```
.
└── business_entities_schemas
    ├── init.py 
    ├── business_entity1
    │   ├── business_entity1_v1.json
    │   └── business_entity1_v2.json    
    └── business_entity2
```

You can also refer to the sample in the default [Herbie schema repostory](https://github.com/project-a/herbie-json-schema) as a guideline.

This sample contains schema definitions for the business entities 'customer' and 'product':

```
.
└── herbie-json-schema
    ├── init.py
    ├── customer
    │   ├── customer_v1.json
    │   └── customer_v2.json    
    └── product
        └── product_v1.json
```



### 2.1 Using a Separate Github Repository

1. Create a new GitHub repository for and commit your schema files according to the previously described package structure.
1. In your main Herbie repository, update the dependencies so that Herbie uses your new schema package. 

    * In [`requirements.txt`](./requirements.txt), locate the following line and replace it with the location of your schema package.
    
        `git+https://github.com/project-a/herbie-json-schema.git`

        For example:
    
        `git+https://github.com/treesus/treesus-schemas.git`

    * In [`herbie/settings.py`](herbie_core/settings.py), locate the variable `SCHEMA_REGISTRY_PACKAGE` variable and update the value with the name of your package.

       For example:
       ```
       # Json schema package for validation of business objects
       SCHEMA_REGISTRY_PACKAGE = 'treesus_schemas'
       ````

    > **_NOTE:_** If you're storing your schemas in a _private_ repository, make sure that you provide the `herbie-app` container with a private ssh key. Then, ensure that you use the ssh to clone the repository on the `herbie-app` container. Otherwise, Herbie will not be able to access your JSON schemas. <br/><br/>
    During development, it's OK to use a personal ssh key. However, for production, we recommend that you create a dedicated ssh key for the Herbie app.

### 2.2 Storing the schemas package in the main Herbie repository
1. In the root folder of your Herbie respository, commit your schema files according to the previously described package structure.
1. In [`herbie/settings.py`](herbie_core/settings.py), locate the variable `SCHEMA_REGISTRY_PACKAGE` variable and update the value with the name of your package.

       For example:
       ```
       # Json schema package for validation of business objects
       SCHEMA_REGISTRY_PACKAGE = 'treesus_schemas'
       ````

# Run Herbie on Docker
1. Clone the project (from your forked version or from the official repository)
1. Build and run Herbie
```
docker-compose -f docker-compose-google-pubsub.yml up -d
```
- Connect to herbie-app container
```
docker exec -it herbie-app bash
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
        
     > NOTE: If you're using Google Pub/Sub run the following extra command: `python manage.py init_pubsub` 




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

## Changing the messaging system
The default Herbie setup uses Kafka (mainly because it's very popular) for distributing
the business entity messages in a JSON format. But it should be easy to use any other
messaging system:

The messaging is implemented in
[herbieapp/services/message_publisher.py](herbieapp/services/message_publisher/message_publisher.py).
To replace the Kafka client with any other client, you just have to change the
implementation of the internal `_send_message` method of the `MessagePublisher` class.

Then you can also remove or replace the Kafka connection settings in
[herbie/settings.py](herbie_core/settings.py), and also remove or replace the Kafka and
Zookeeper images in the [docker-compose.yml](legacy/docker-compose-kafka.yml).


## Herbie - Development
- [PyCharm Configuration](docs/pycharm_config.md)
