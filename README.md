# Herbie

[![CI Build](https://github.com/herbie/herbie/workflows/CI/badge.svg?branch=master)](https://github.com/herbie/herbie/actions?query=workflow%3ACI)

## What is Herbie?
Herbie is an abstract data layer that makes it easier to exchange data across distributed systems. You define business entities such as “customer” or “order” as JSON schemas which you store in a central schema registry. Herbie can listen for data updates in one system and publish new data to other systems based on your business rules. 

## Why should you use Herbie
It simplifies the process of building integrations and connectors for all your systems. Maybe you want to build a connector between MailChimp and Salesforce, but also between MailChimp and Shopify, and maybe also between Salesforce and Shopify. Each time, you have to customize your connector to the requirements of the two systems. What if all your systems connected to one central data layer? - that’s Herbie. 
 
Once all your systems are connected to Herbie, they can then talk to one another. Once the system can subscribe to changes in another system. Just updated your contacts in Salesforce? Your MailChimp connector can listen for the changes and update the Mailchimp database accordingly.


## Overview

Herbie uses a _schema registry_ combined with a _central data store_ for business 
entities.
* It's built with _Django_ and comes with a simple API to create business entities.
* The _json-schema_ integration allows you to define custom schema definitions which Herbie uses to validate the entities. 
* By default, we provide support for _Google Pub/Sub_ or _AWS SNS/SQS_ to provide _event streams_ — your services can subscribe to these event streams and find out when a certain entity-type is updated.

    However, you don't have to use Google Pub/Sub - you can also update Herbie to [use your preferred messaging system](#changing-the-messaging-system).

The philosophy behind Herbie is to avoid behavior that seems like a "black box" and is instead built in very
straightforward way, following Django best practices. It is also meant to be extendable and easy to adapt.

**Further reading:**

- [Core Concepts](docs/core_concepts.md)



## Getting started

#### Quick Start

The easiest and recommended way to start a new project is to clone the [sandbox](https://github.com/herbie/sandbox) repository and follow the instructions.


#### Step by step guide

1. Herbie is based on the Django framework, so the first step is to start a [new Django project](https://www.djangoproject.com/start/) using **postgres** as database technology.

1. After the Django-skeleton is set up, Herbie can be installed using a common package manager like pip.

    ```
    python -m pip install herbie
    ```
   
   You can also add Herbie to your `requirements.txt`.

1. The next step is to configure the settings accordingly:
    
    a) Register Herbie and the django rest-framework in your installed apps.
    
    ```python
    INSTALLED_APPS = [
        # ...
        'rest_framework',
        'rest_framework.authtoken',
        'herbie_core.apps.HerbieCoreConfig',
    ]
    ```
    
    b) Setup the token-authentication for the provided Herbie-API:

    ```python
    REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': (
           'rest_framework.authentication.TokenAuthentication',
       ),
    }
    ```
   
    c) Define Schema package
    
    d) Select a Queueing technology (AWS SNS/SQS vs. Google Pubsub)
    
    e) Register herbie urls in your urls.py:
    ```python
    from herbie_core import urls as herbie_urls
    
    urlpatterns = [
    # ...
        path('api/', include(herbie_urls)),
    ]
    ```

1. Add schemas by either adding them to the remote repository or to a local package.

1. Run the Django-App in preferred way-> link

1. When app is running execute the following commands:
    
    1. Generate model classes for the sample business objects that are included in the Herbie [schemas package](https://github.com/project-a/herbie-json-schema).
  
        ```
        python manage.py generatemodels
        ```
    1. Create and execute migration files to initialize your database
  
        ```
        python manage.py makemigrations
        python manage.py migrate
        ```
    1. Load the schemas to the database:
       ```
       python manage.py import_json_schemas
       ```
    
    1. Create an admin user so that you can log in to the admin dashboard.
       ```
       python manage.py createsuperuser --username "username" --email "email@email-address.com"
       ```

#### Changing the messaging system
By default [Herbie sandbox](https://github.com/herbie/sandbox) setup uses _Google Pubsub_ for distributing
the business entity messages in a JSON format. But it should be easy to use any other
messaging system:

The different messaging systems are distributed as Python packages and are also based on Django. To use or add a new one it is as
easy as registering a new Django app.

Check [Google Pubsub adapter](https://github.com/herbie/google-pubsub-adapter) repository for detailed instructions.


#### Admin Panel
- [How to add social login?](docs/social_login.md)
