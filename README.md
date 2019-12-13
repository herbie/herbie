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



## Create Social api key and secret (google,github, etc.)

1. Create an oauth api on Google/Github
2. Save the auto-generated credentials (key/secret) in environment variables
3. add the credentials to settings.py

#### Google

`SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env.str('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')`

`SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env.str('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')`


#### Github

`SOCIAL_AUTH_GITHUB_KEY = env.str('SOCIAL_AUTH_GITHUB_KEY')`
`SOCIAL_AUTH_GITHUB_SECRET = env.str('SOCIAL_AUTH_GITHUB_SECRET')`

###### Helpful Tutorials

https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html
https://medium.com/trabe/oauth-authentication-in-django-with-social-auth-c67a002479c1
