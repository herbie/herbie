# Add Auth Token for a Service

##### 1) Create a super user
```
python manage.py createsuperuser --username "username" --email "email-address"
```
##### 2) Log in to the admin panel as super user  
```
http://localhost:8000/admin
```
##### 3) Create user with username, the name of the service

##### 4) Go to Users in the admin panel and choose your new user-service

##### 5) Go to the (permissions section -> User permissions) and add Permissions
```
Each business entity represent a channel/topic and has 
4 different permissions (add, change, delete, view)

Example for Customer business entity:
wayneapp | customer | Can add customer
wayneapp | customer | Can change customer
wayneapp | customer | Can delete customer
wayneapp | customer | Can view customer

For save requests (api/<business_entity>/save) you need to have both add and change permissions 
```

##### 5) Create a token for your new user-service
```
Go to Tokens -> add Token -> choose your new user-service -> save
```

##### 5) How to add the token in the requests
```
add it in the headers of the request 
Authorization: Token "token-value"
Example:
Authorization: Token 9054f7aa9305e012b3c2300408c3dfdf390fcddf
```