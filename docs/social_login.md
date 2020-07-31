# Social Login for Admin Panel

## Dependencies

Social login is set as an optional dependency and not enabled by default.

#### Installing/enabling dependencies

1. Add to `requirements.txt` or `pip install` the following packages:

    ```
        social-auth-app-django
    ```

2. Register the package in Django installed apps:s
    
    ```python
    INSTALLED_APPS = [
        # ...
        'social_django',
    ]
    ```

## Create Social api key and secret (google,github, etc.)


#### Google

1. Obtain OAuth 2.0 client credentials from the Google API Console
2. Add the auto-generated credentials (key/secret) as environment variables
3. Add the credentials to settings.py


`SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env.str('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')`

`SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env.str('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')`


#### Github

`SOCIAL_AUTH_GITHUB_KEY = env.str('SOCIAL_AUTH_GITHUB_KEY')`

`SOCIAL_AUTH_GITHUB_SECRET = env.str('SOCIAL_AUTH_GITHUB_SECRET')`

###### Helpful Tutorials

https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html
https://medium.com/trabe/oauth-authentication-in-django-with-social-auth-c67a002479c1
